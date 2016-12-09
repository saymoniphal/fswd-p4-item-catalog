from flask import render_template

from run import app

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login-form.html')
