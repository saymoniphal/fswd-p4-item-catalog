#!/bin/bash/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey

Base = declarative_base()

class Catalog(Base):
    """Class represents table 'catalog' in the database which has attributes:
    name: name of the catalog
    description: description in text of the catalog
    catalog_id: the id number of the catalog
                (incrementally assigned by the database)
    """

    # table name in the database
    __tablename__ = 'catalogs'

    # attributes which represents each column in the table
    catalog_id = Column(Integer, Sequence('catalog_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    owner = Column(String(50))


class Item(Base):
    """Class represents table 'item' in the database which has attributes:
    name: name of the item, it should not be empty
    description: description in text of the item
    item_id: the id number of the item (incrementally assigned by the database)
    catalog_id: the id number of the catalog (refer to catalogs) 
    """

    # table name in the database
    __tablename__ = 'items'

    # attributes which represents each column in the table
    item_id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    catalog_id = Column(Integer, ForeignKey('catalogs.catalog_id')) 
    owner = Column(String(50))


def create_db():
    """Connect to the database and create the database schema"""
    engine = create_engine('sqlite://item_catalog.db', echo=True)
    
    
def main():
    pass


if __name__ == '__main__':
    main()
