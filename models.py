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


@contextmanager
def session_scope():
    """Return session as database handle via engine connection.
    Provide transactional scope for the session.
    Use context manager decorator so it can be called via 'with', the session 
    will be committed and close on sucess, rollback on failure and close""" 

    session = None 
    try:
       session = DBSession()
       yield session
       session.commit()
    except:
       if session:
           session.rollback()
       raise
    finally:
       if session:
           session.close()
 
    
def deleteCategory(c_id):
    with session_scope() as session:
       cat_obj = session.query(Category).filter_by(category_id=c_id).one()
       session.delete(cat_obj)


def addCategory(name, user_id, description=None):
    """Adds the category to the database and returns its <id number>"""
    id = 0 
    c = Category(name=name, user_id=user_id, description=description)
    with session_scope() as session:
       session.add(c)
       # flush object 'c' to DB, so that its auto-inc id will be generated
       session.flush()
       id = c.category_id
    return id 

def editCategory(category_id, name, description=None):
    with session_scope() as session:
       cat = session.query(Category).filter_by(category_id=category_id).one()
       cat.name = name
       if description:
          cat.description = description
       session.add(cat)


def getCategory(category_id):
    c = None
    with session_scope() as session:
      c = session.query(Category).filter_by(category_id=category_id).one()
    return c

 
def deleteItem(item_id):
    with session_scope() as session:
       item_obj = session.query(Item).filter_by(item_id=item_id).one()
       session.delete(item_obj)


def addItem(name, category_id, user_id, description=None):
    """Adds the item entry to the database and returns its <id number>"""
    item = Category(name=name, category_id=category_id, user_id=user_id,
                   description=description)
    with session_scope() as session:
       session.add(item)
       # flush object 'item' to DB, so that its auto-inc id will be generated
       session.flush()
       return item.item_id


def editItem(item_id, name, description=None):
    with session_scope() as session:
       item = session.query(Item).filter_by(item_id=item_id).one()
       item.name = name
       if description:
          item.description = description
       session.add(item)


def createUser(login_session):
    """Create User object and save to the database. Returns the id number of
    the newly added user"""

    newUser = User(name=login_session['username'], email=login_session['email'])
    with session_scope() as session:
       session.add(newuser)
       session.flush()
       #user = session.query(User).filter_by(email=login_session['email']).one()
       return user.user_id

def getUserId(email):
    user_id = None
    with session_scope() as session:
       user = session.query(User).filter_by(email=email).one()  
       user_id = user.id
    return user_id


def getUserInfo(user_id):
    user = None
    with session_scope() as session:
       user = session.query(User).filter_by(user_id=user_id).one()
    return user 


def main():
    pass


if __name__ == '__main__':
    main()
