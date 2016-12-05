#!/bin/bash/env python

from flask import Flask, session
from flask import request, redirect, url_for, render_template

app = Flask(__name__, template_folder='templates')

# Decorator that route "/" and "/item_catalog" with below function
@app.route("/")
@app.route("/item_catalog")
def index():
    return render_template("index.html")


def main():
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
