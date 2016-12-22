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
        redirect(url_for('showlogin'))


@app.route('/category/new', methods=["GET", "POST"])
def newCategory():
    """Add a new category"""
    check_user()
    if request.method == 'POST':
        newCategory = models.addCategory(name=login_session['name'],
                                 user_id=login_session['username'],
                                 description=login_session['description'])
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('newCategory.html')


@app.route('/category/<int:category_id>/edit', methods=["GET", "POST"])
def editCategory(category_id):
    """Edit a new category"""
    check_user() 
    if request.method == 'POST':
        if request.form['name']:
	        name = request.form['name']
        if request.form['description']:
            description = request.form['description']
        models.editCategory(category_id=category_id, name=name,
                            description=description)
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('editCategory.html')


@app.route('/category/<int:category_id>/delete', methods=["GET", "POST"])
def deleteCategory(category_id):
    check_user()
    if request.method == 'POST':
        models.deleteCategory(category_id)
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('deleteCategory.html')

@app.route('/')
@app.route('/category/all')
def showAllCategories():
    categories = models.getAllCategories()
    return render_template('index.html', categories=categories)


@app.route('/category/<int:category_id>/show')
def showCategory(category_id):
    c = models.getCategory(category_id)
    return render_template('category.html', category=c) 
