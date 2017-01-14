from flask import render_template, request, redirect
from flask import url_for, abort, jsonify
from flask import session as login_session

from catalog import app, login_required
import models


@app.route('/item/<int:category_id>/new', methods=["GET", "POST"])
@login_required
def newItem(category_id):
    """Add a new item"""
    sess = models.connect_db(app.db_uri)
    category = models.Category.getById(sess, category_id)
    # abort in case the user is not the owner of the category
    if category.user.name != login_session['username']:
        abort(403)

    if request.method == 'POST':
        models.Item.create(sess, request.form['name'],
                           category,
                           request.form['description'])
        sess.commit()
        return redirect(url_for('showCategory',
                                category_id=category.category_id))
    else:
        return render_template('newItem.html',
                               item=None,
                               cat=category,
                               login_session=login_session)


@app.route('/item/<int:item_id>/edit', methods=["GET", "POST"])
@login_required
def editItem(item_id):
    """Edit an item"""
    sess = models.connect_db(app.db_uri)
    item = models.Item.getById(sess, item_id)
    categories = models.Category.all(sess)
    if item.category.user.name != login_session['username']:
        abort(403)

    if request.method == 'POST':
        category_id = item.category.category_id
        if request.form['post_action'] == 'save_item':
            item.name = request.form['name']
            item.description = request.form['description']
            if request.form['categoryid'] != category_id:
                cat = models.Category.getById(sess, request.form['categoryid'])
                item.category = cat
            sess.add(item)
            sess.commit()
        return redirect(url_for('showItem', item_id=item.item_id))
    else:
        return render_template('newItem.html',
                               item=item,
                               cat=item.category,
                               categories=categories,
                               login_session=login_session)


@app.route('/item/<int:item_id>/delete', methods=["GET", "POST"])
@login_required
def deleteItem(item_id):
    """Delete an item"""
    sess = models.connect_db(app.db_uri)
    item = models.Item.getById(sess, item_id)
    if item.category.user.name != login_session['username']:
        abort(403)

    if request.method == 'POST':
        if request.form['post_action'] == 'delete_item':
            sess.delete(item)
            sess.commit()
            return redirect(url_for('showCategory',
                                    category_id=item.category.category_id))
        else:
            return redirect(url_for('showItem',
                                    item_id=item.item_id))
    else:
        return render_template('deleteItem.html',
                               item=item,
                               login_session=login_session)


@app.route('/item/<int:item_id>/show')
def showItem(item_id):
    """Show item details"""
    sess = models.connect_db(app.db_uri)
    item = models.Item.getById(sess, item_id)
    return render_template('itemdetail.html',
                           item=item, login_session=login_session)


@app.route('/item/<int:item_id>/json')
def item(item_id):
    """Generate JSON representation of item"""
    sess = models.connect_db(app.db_uri)
    item = models.Item.getById(sess, item_id)
    return jsonify(item.serialize)
