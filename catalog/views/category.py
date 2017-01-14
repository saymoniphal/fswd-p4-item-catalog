from flask import render_template, request, redirect
from flask import url_for, abort, jsonify
from flask import session as login_session

from catalog import app, login_required
import models


@app.route('/category/new', methods=["GET", "POST"])
@login_required
def newCategory():
    """Add a new category"""
    sess = models.connect_db(app.db_uri)
    user = models.User.getByName(sess, login_session['username'])
    if request.method == 'POST':
        if request.form['post_action'] == 'save_category':
            newCategory = models.Category.create(sess,
                                                 request.form['name'],
                                                 user,
                                                 request.form['description'])
            sess.commit()
            return redirect(url_for('showCategory',
                                    category_id=newCategory.category_id))
        else:
            return redirect(url_for('showAllCategories'))
    else:
        return render_template('newCategory.html',
                               cat=None,
                               login_session=login_session)


@app.route('/category/<int:category_id>/edit', methods=["GET", "POST"])
@login_required
def editCategory(category_id):
    """Edit a category"""
    sess = models.connect_db(app.db_uri)
    cat = models.Category.getById(sess, category_id)
    if cat.user.name != login_session['username']:
        abort(403)
    if request.method == 'POST':
        if request.form['post_action'] == 'save_category':
            cat.name = request.form['name']
            cat.description = request.form['description']
            sess.add(cat)
            sess.commit()
        return redirect(url_for('showCategory', category_id=category_id))
    else:
        return render_template('newCategory.html',
                               cat=cat,
                               login_session=login_session)


@app.route('/category/<int:category_id>/delete', methods=["GET", "POST"])
@login_required
def deleteCategory(category_id):
    """Delete a category"""
    sess = models.connect_db(app.db_uri)
    cat = models.Category.getById(sess, category_id)
    if cat.user.name != login_session['username']:
        abort(403)

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


@app.route('/category/<int:category_id>/json')
def category(category_id):
    """Return JSON representation of category and items"""
    sess = models.connect_db(app.db_uri)
    c = models.Category.getById(sess, category_id)
    return jsonify(c.serialize)


@app.route('/category/<int:category_id>/show')
def showCategory(category_id):
    """Show details of a category"""
    sess = models.connect_db(app.db_uri)
    categories = models.Category.all(sess)
    c = models.Category.getById(sess, category_id)
    return render_template('catdetail.html',
                           sel_category=c,
                           all_categories=categories,
                           login_session=login_session)


@app.route('/')
@app.route('/category/all')
def showAllCategories():
    """Show all categories"""
    sess = models.connect_db(app.db_uri)
    categories = models.Category.all(sess)
    sel_category = None
    if len(categories) > 0:
        sel_category = categories[0]
    return render_template('catdetail.html',
                           sel_category=sel_category,
                           all_categories=categories,
                           login_session=login_session)
