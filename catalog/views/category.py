from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint
from flask import session as login_session

import random, string

from catalog import app
import models

# create a blueprint with name 'category'
#category_app = Blueprint('category_app', __name__)


def check_user():
    if 'username' not in login_session:
        return redirect(url_for('showlogin'))


@app.route('/category/new', methods=["GET", "POST"])
def newCategory():
    """Add a new category"""
    check_user()
    sess = models.connect_db(app.db_uri)()
    user = models.User.getByName(sess, login_session['username'])
    if request.method == 'POST':
        newCategory = models.Category.create(sess,
                                             request.form['name'],
                                             user,
                                             request.form['description'])
        sess.commit()
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('newCategory.html',
                               login_session=login_session)


@app.route('/category/<int:category_id>/edit', methods=["GET", "POST"])
def editCategory(category_id):
    """Edit a new category"""
    check_user()
    sess = models.connect_db(app.db_uri)()
    cat = models.Category.getById(sess, category_id)
    if request.method == 'POST':
        if request.form['name']:
            cat.name = request.form['name']
        if request.form['description']:
            cat.description = request.form['description']
        sess.add(cat)
        sess.commit()
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('newCategory.html',
                               login_session=login_session)


@app.route('/category/<int:category_id>/delete', methods=["GET", "POST"])
def deleteCategory(category_id):
    check_user()
    sess = models.connect_db(app.db_uri)()
    cat = models.Category.getById(sess, category_id)
    if request.method == 'POST':
        session.delete(cat)
        session.commit()
        return redirect(url_for('showAllCategories'))
    else:
        return render_template('deleteCategory.html',
                               login_session=login_session)


@app.route('/category/<int:category_id>/show')
def showCategory(category_id):
    sess = models.connect_db(app.db_uri)()
    c = models.Category.getById(sess, category_id)
    return render_template('category.html', category=c,
                           login_session=login_session)

@app.route('/')
@app.route('/category/all')
def showAllCategories():
    sess = models.connect_db(app.db_uri)()
    categories = models.Category.all(sess)
    return render_template('index.html', categories=categories,
                           login_session=login_session)
