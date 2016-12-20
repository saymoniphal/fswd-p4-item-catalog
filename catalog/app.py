import flask
from flask import Flask, render_template, request, jsonify
from flask import session as login_session
import httplib2
from oauth2client import client

import json
import random
import string

import models

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')


# Decorator that route "/" and "/item_catalog" with below function
@app.route("/")
@app.route("/item_catalog")
def index():
    return render_template("index.html")


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
    """Generate anti-forgery state token"""
    state = ''.join(random.choice(string.ascii_lowercase +
                                  string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/googleconnect', methods=['POST'])
def googleconnect():
    """client must have received authorization code from Google API server.
       This code on the server will exchange auth-code (one-time-use) with
       Google API server for user credential (access_token and id_token)"""

    #1. verify anti-forgery state token received from client
    if login_session['state'] != request.args.get('state'):
        # invalid state token
        return response('Invalid sesssion parameter.', 401)

    try:
    #2. exchange one-time-use code with Google API server for access_token
        # get oauth 'Flow' object
        oauth_flow = client.flow_from_clientsecrets(
                                   app.config['CLIENT_SECRET_FILE'], scope='')
        # add redirect_uri since it's required by Google API server, but since
        # it's not really being used, any value should be okay
        # 'postmessage' or 'https://www.example.com/oauth2callback' works
        oauth_flow.redirect_uri = 'https://www.example.com/oauth2callback' 

        # exchange authorization code for credentials
        auth_code = request.data
        credentials = oauth_flow.step2_exchange(auth_code)
        print("auth_code: {code}".format(code=auth_code)) #DEBUG

    except client.FlowExchangeError:
        return response('Fail to get user credentials.', 401)

    #3. Validate access_token with Google API server
    access_token = credentials.access_token
    print("access_token: {code}".format(code=access_token)) #DEBUG
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?' +
           'access_token=%{t}'.format(t=access_token))
    h = httplib2.Http()
    g_resp = h.request(url, 'GET')
    authorized_token = json.loads(g_resp[1])
    
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
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    #4. Get user information
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token,
              'alt': json}
    resp = request.get(uerinfo_url, params=params)
    user_data = resp.json

    login_session['username'] = user_data['username']
    login_session['email'] = user_data['email']
    login_session['picture'] = user_data['picture']

    print("authentication done: username:%s" %(user_data['username'],)) #DEBUG
    # all done
    return render_template('index.html', login_session=login_session)


def response(content, errorcode):
    response = flask.make_response(json.dumps(content), errorcode)
    response.headers['Content-Type'] = 'application/json'
    return response
