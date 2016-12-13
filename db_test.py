import unittest
import pprint

from models import *

class TestDBConnection(unittest.TestCase):

    DBSession = None
    user_id = 1


    @classmethod
    def setup(self):
       DBSession = models.connect_db('sqlite:///:memory:')


    def test_category(self):
       id1 = addCategory(name='category1', user_id=1,
                             description='This is category1')
       c1 = getCategory(id1)
       print(c1.name)
       pprint.pprint(c1.serialize)
       self.assertEqual(c1, { 'name' : 'category1', 'user_id' : 1,
                              'description' : 'This is category1' })
       addCategory(name='category2', user_id=1) # no description
       addCategory(name='category3', user_id=1, description='This is category3')
       addCategory(name='category4', user_id=1, description='This is cat4')


if __name__ == '__main__':
    unittest.main()
