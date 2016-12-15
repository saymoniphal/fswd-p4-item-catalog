import flask

from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
#app.register_blueprint(category_app)

import models

# Decorator that route "/" and "/item_catalog" with below function
@app.route("/")
@app.route("/item_catalog")
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    # generate random string of length 32 to be used as session state
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32)) 
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/help')
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

