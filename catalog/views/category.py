from flask import render_template, request, flash
from flask import Blueprint
from flask import session as login_session

import random, string

from catalog import app
import models

# create a blueprint with name 'category'
#category_app = Blueprint('category_app', __name__)


def check_user():
    if 'username' not in login_session:
        redirect(url_for('/login')


@app.route('/category/new', methods=["GET", "POST"])
def newCategory():
    """Add a new category"""
    check_user()
    if request.method == 'POST':
        newCategory = models.addCategory(name=login_session['name'],
                                 user_id=login_session['username'],
                                 description=login_session['description'])
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit', methods=["GET", "POST"])
def editCategory(category_id):
    """Edit a new category"""
    check_user() 
    if request.method == 'POST':
        category = models.editCategory(category_id=category_id,
                                name=request.('name'),
                                description=login_session['description'],
                                user_id=login_session('username'))
        return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html')

@app.route('/category/<int:category_id>/delete', methods=["GET", "POST"])
def deleteCategory(category_id):
    check_user()
    if request.method == 'POST':
        models.deleteCategory(category_id)
        return redirect(url_for('showCategories')
    else:
        return render_template('deleteCategory.html')
