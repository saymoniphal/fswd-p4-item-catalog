#!/bin/bash/env python3

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from dbsetup import User, Category, Item


def connect_db(db_url):
    """Connect to the database and create the database schema"""

    # create an engine connecting the database
    engine = create_engine(db_url, echo=True)
    DBSession = sessionmaker(bind=engine)
    return DBSession 


DBSession = connect_db('sqlite:///itemcatalog.db')
session = DBSession()


def add_to_db(orm_obj):
    """Add given object to the session and commit to the database,
        rollback transaction in case of failure"""
    try:
        if session:
            session.add(orm_obj)
            session.commit()
    except:
        if session:
            session.rollback()
        raise

    
def delete_from_db(orm_obj):
    """Delete given object to the session and commit to the database,
        rollback transaction in case of failure"""
    try:
        session.delete(orm_obj)
        session.commit()
    except:
        session.rollback()


def getORM(obj_name, filter_by, filter_v):
    """Return ORM object with data from database"""
    d = {'User': User, 'Item': Item, 'Category': Category}
    args = {filter_by:filter_v}
    return session.query(d[obj_name]).filter_by(**args).first()
    

def addCategory(name, user_id, description=None):
    """Adds the category to the database and returns its <id number>"""
    c = Category(name=name, user_id=user_id, description=description)
    add_to_db(c)
    return c.category_id 


def getCategory(c_id):
    return getORM(obj_name='Category', filter_by='category_id', filter_v=c_id)


def editCategory(category_id, name, description=None):
    c = getCategory(category_id)
    c.name = name
    if description:
       c.description = description
    add_to_db(c)


def deleteCategory(c_id):
    c = getCategory(c_id)
    delete_from_db(c)


def addItem(name, category_id, user_id, description=None):
    """Adds the item entry to the database and returns its <id number>"""
    item = Item(name=name, category_id=category_id, user_id=user_id,
                   description=description)
    add_to_db(item)
    return item.item_id 


def getItem(item_id):
    return getORM(filter_by='item_id', filter_v='item_id', obj_name='Item')


def editItem(item_id, name, description=None):
    item = getItem(item_id)
    item.name = name
    if description:
       item.description = description
    add_to_db(item) 


def deleteItem(item_id):
    item = getItem(item_id)
    delete_from_db(item)


def createUser(login_session):
    """Create User object and save to the database. Returns the id number of
    the newly added user"""

    user = getORM(filter_by='email', filter_v=login_session['email'],
                    obj_name='User')
    if user: # user already exist, don't add again
        return user.user_id

    newUser = User(name=login_session['username'], email=login_session['email'])
    add_to_db(newUser)
    return newUser.user_id


def getUserId(email):
    user = getORM(obj_name='User', filter_by='email', filter_v=email)
    if user:
        return user.user_id
    return None


def getUser(user_id):
    return getORM(filter_by='user_id', filter_v='user_id', obj_name='User')
