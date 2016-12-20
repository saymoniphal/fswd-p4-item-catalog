import unittest
import pprint

import models

class TestDBConnection(unittest.TestCase):

    DBSession = None
    user_id = 1


    @classmethod
    def setup(self):
        DBSession = models.connect_db('sqlite:///itemcatalog.db')


    def test_user(self):
        user_id = models.createUser({'username':'user1', 'email':'user1@email.com'})
        user = models.getUserInfo(user_id)
        self.assertEqual(user.name, 'user1')
        self.assertEqual(user.email, 'user1@email.com') 

    def test_category(self):
        id1 = models.addCategory(name='category1', user_id=1,
                             description='This is category1')
        print("category_id: %s" %(id1))
        c1 = models.getCategory(id1)
        print "c1.name: " + c1.name
        pprint.pprint(c1.serialize)
        self.assertEqual(c1.name, 'category1')
        self.assertEqual(c1.user_id, 1)
        self.assertEqual(c1.description, 'This is category1')

        models.addCategory(name='category2', user_id=1) # no description
        models.addCategory(name='category3', user_id=1,
                            description='This is category3')
        models.addCategory(name='category4', user_id=1,
                            description='This is cat4')


if __name__ == '__main__':
    unittest.main()
