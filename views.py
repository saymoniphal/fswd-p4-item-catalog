from flask import render_template
from flask import request
from flask import session as login_session

from models import *
from run import app

@app.route('/category/new', methods=["GET", "POST"])
def newCategory():
    """Add a new catalog"""
    # TODO:need to check for authenticate user
    if request.method == 'POST':
        newCategory = addCategory(login_session['name'],
                                 login_session['username'],
                                 login_session['description'])
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
