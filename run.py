#!/bin/bash/env python

from flask import Flask, render_template
from models import *
from views import *

app = Flask(__name__, template_folder='templates')
app.config.from_object('config')
app.register_blueprint(category_app)

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


def main():
    app.secret_key = app.config['SECRET_KEY']
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
