from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint
from flask import session as login_session

import random, string

from catalog import app
import models


def check_user():
    """Check if user is logged in"""
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
                               cat=None,
                               login_session=login_session)


@app.route('/category/<int:category_id>/edit', methods=["GET", "POST"])
def editCategory(category_id):
    """Edit a new category"""
    check_user()
    sess = models.connect_db(app.db_uri)()
    cat = models.Category.getById(sess, category_id)
    if request.method == 'POST':
        if request.form['post_action'] == 'save_category':
            if request.form['name']:
                cat.name = request.form['name']
            if request.form['description']:
                cat.description = request.form['description']
            sess.add(cat)
            sess.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newCategory.html',
                               cat=cat,
                               login_session=login_session)


@app.route('/category/<int:category_id>/delete', methods=["GET", "POST"])
def deleteCategory(category_id):
    check_user()
    sess = models.connect_db(app.db_uri)()
    cat = models.Category.getById(sess, category_id)
    if request.method == 'POST':
        if request.form['post_action'] == 'delete_category':
            sess.delete(cat)
            sess.commit()
            return redirect(url_for('showAllCategories'))
        else:
            return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('deleteCategory.html',
                               cat=cat,
                               login_session=login_session)


@app.route('/category/<int:category_id>/show')
def showCategory(category_id):
    sess = models.connect_db(app.db_uri)()
    categories = models.Category.all(sess)
    c = models.Category.getById(sess, category_id)
    return render_template('catdetail.html',
                           sel_category=c,
                           all_categories=categories,
                           login_session=login_session)

@app.route('/')
@app.route('/category/all')
def showAllCategories():
    sess = models.connect_db(app.db_uri)()
    categories = models.Category.all(sess)
    return render_template('catdetail.html',
                           sel_category=None,
                           all_categories=categories,
                           login_session=login_session)
