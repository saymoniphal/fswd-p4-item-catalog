#!/bin/bash/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy import sessionmaker

Base = declarative_base()
DBSession = connect_db()

class User(Base):
    """Represents 'users' table in the database with attributes:
    user_id: the id number of the user (generated by the DB)
    name: name of the user
    email: email address of the user
    """

    # table name in the database
    __tabalename__ = 'users'

    # attributes which corespond to each column in the table
    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

class Category(Base):
    """Class represents table 'category' in the database which has attributes:
    name: name of the category
    description: description in text of the category
    category_id: the id number of the category
                (incrementally assigned by the database)
    user_id: the id number of the user created the category (foreign key)
    """

    # table name in the database
    __tablename__ = 'categories'

    # attributes which represents each column in the table
    category_id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.user_id') 
    user = Relationship("User")


class Item(Base):
    """Class represents table 'item' in the database which has attributes:
    name: name of the item, it should not be empty
    description: description in text of the item
    item_id: the id number of the item (incrementally assigned by the database)
    category_id: the id number of the category (refer to categories)
    user_id: the id number of the user created the category (foreign key)
    """

    # table name in the database
    __tablename__ = 'items'

    # attributes which represents each column in the table
    item_id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.category_id')) 
    user_id = Column(Integer, ForeignKey('users.user_id') 
    user = Relationship("User")


def connect_db():
    """Connect to the database and create the database schema"""

    # create an engine connecting the database
    engine = create_engine('sqlite://item_catalog.db', echo=True)
    DBSession = sessionmaker(bind=engine)
    return DBSession 


@contextlib.contextmanager
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
 
    
def addCategory(name, user_id, description=None):
    cat = Category(name=name, owner=owner, description=description)
    with session_scope() as session:
       session.add(cat)


def addItem(name, category, user_id, description=None):
    cat = Category(name=name, category_id=category, owner=owner,
                   description=description)
    with session_scope() as session:
       session.add(cat)


def get_user_byid(user_id):
    user = None
    with session_scope() as session:
       user = session.query(User).filter_by(user_id=user_id).one()  
    return user


def get_user_email(user_id):
    with session_scope() as session:
       user = session.query(User).filter_by(user_id=user_id).one()
    return user.email 


def main():
    pass


if __name__ == '__main__':
    main()
