#!/bin/bash/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey

Base = declarative_base()

class Category(Base):
    """Class represents table 'category' in the database which has attributes:
    name: name of the category
    description: description in text of the category
    category_id: the id number of the category
                (incrementally assigned by the database)
    """

    # table name in the database
    __tablename__ = 'categories'

    # attributes which represents each column in the table
    category_id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    owner = Column(String(50))


class Item(Base):
    """Class represents table 'item' in the database which has attributes:
    name: name of the item, it should not be empty
    description: description in text of the item
    item_id: the id number of the item (incrementally assigned by the database)
    category_id: the id number of the category (refer to categories)
    """

    # table name in the database
    __tablename__ = 'items'

    # attributes which represents each column in the table
    item_id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    category_id = Column(Integer, ForeignKey('category.category_id')) 
    owner = Column(String(50))


def create_db():
    """Connect to the database and create the database schema"""
    engine = create_engine('sqlite://item_catalog.db', echo=True)
    
    
def main():
    pass


if __name__ == '__main__':
    main()
