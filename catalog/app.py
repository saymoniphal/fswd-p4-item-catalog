from functools import wraps

import flask
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import session as login_session
import requests
from oauth2client import client

import json
import random
import string

import models

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showlogin'))
        return f(*args, **kwargs)
    return decorated_function


# Decorator that route "/" and "/item_catalog" with below function
@app.route("/")
@app.route("/item_catalog")
def index():
    return redirect(url_for('showAllCategories')) 


@app.route('/help')
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)


@app.route('/login')
def showlogin():
    """Login a user"""
    state = ''.join(random.choice(string.ascii_lowercase +
                                  string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,
                           login_session=login_session)


@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    """client must have received authorization code from Google API
       server.  This code on the server will exchange auth-code
       (one-time-use) with Google API server for user credential
       (access_token and id_token)"""

    #1. verify anti-forgery state token received from client
    if login_session['state'] != request.args.get('state'):
        # invalid state token
        return response('Invalid sesssion parameter.', 401)

    try:
        #2. exchange one-time-use code with Google API server for
        # access_token get oauth 'Flow' object
        oauth_flow = client.flow_from_clientsecrets(
                                   app.config['CLIENT_SECRET_FILE'], scope='')
        # add redirect_uri since it's required by Google API server,
        # but since it's not really being used, any value should be
        # okay 'postmessage' or
        # 'https://www.example.com/oauth2callback' works
        oauth_flow.redirect_uri = 'postmessage'

        # exchange authorization code for credentials
        auth_code = request.data
        credentials = oauth_flow.step2_exchange(auth_code)

    except client.FlowExchangeError as ex:
        print('failed to get user credentials: %s' % (ex,))
        return response('Fail to get user credentials.', 401)

    #3. Validate access_token with Google API server
    access_token = credentials.access_token
    result = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo',
                          params={'access_token': access_token})
    authorized_token = result.json()

    # verify that user logged-in with access_token is the expected one
    gplus_id = credentials.id_token['sub']
    if authorized_token['user_id'] != gplus_id:
        return response('Token user id does not match with given user ID.', 401)

    # verify client ID
    with open(app.config['CLIENT_SECRET_FILE']) as f:
        client_id = json.load(f)['web']['client_id']
    if authorized_token['issued_to'] != client_id:
        return response('Client ID does not match user app', 401)

    # store credentials and gplus_id in login_session for later use
    login_session['gplus_id'] = gplus_id
    login_session['access_token'] = access_token
    login_session['credentials'] = credentials.to_json()

    #4. Get user information
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token,
              'alt': 'json'}
    resp = requests.get(userinfo_url, params=params)
    user_data = resp.json()

    login_session['username'] = user_data['email']
    login_session['email'] = user_data['email']
    login_session['picture'] = user_data['picture']

    # all done, add user to the database
    sess = models.connect_db(app.db_uri)
    models.User.create(sess, username=login_session['username'],
                           email=login_session['email'])
    sess.commit()
    return redirect(url_for('showAllCategories'))


@app.route('/googledisconnect')
def logout():
    """revoke current user's access_token and reset login session"""
    access_token = login_session.get('access_token', None)
    for key in [ 'access_token', 'gplus_id', 'username',
                 'email', 'picture' ]:
        if key in login_session:
            del login_session[key]
    if not access_token:
        return response('Not logged in', 405)
    url = 'https://accounts.google.com/o/oauth2/revoke'
    res = requests.get(url, params={'token': access_token, 'alt': 'json'})
    if res.status_code != 200:
        # For whatever reason, the given token was invalid.
        print(res.text)
    return redirect(url_for('showAllCategories'))


def response(content, errorcode):
    res = flask.make_response(json.dumps(content), errorcode)
    res.headers['Content-Type'] = 'application/json'
    return res
