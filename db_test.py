import unittest
import pprint

import models

class TestDBConnection(unittest.TestCase):

    DBSession = None

    @classmethod
    def setup(self):
        DBSession = models.connect_db('sqlite:///itemcatalog.db')


    def test_user(self):
        u_id1 = models.createUser({'username':'user1',
                                     'email':'user1@email.com'})
        print "--------------------------------------------------------------------------------"
        print ("USER ID:%d" %(u_id1,))
        print "--------------------------------------------------------------------------------"
        u_id = models.getUserId('user1@email.com')
        print ("-------------USER ID GOT FROM DB BY MAIL: %d" %(u_id,))	
        user = models.getUser(u_id1)
        pprint.pprint(user)
        if user:	
            self.assertEqual(user.name, 'user1')
            self.assertEqual(user.email, 'user1@email.com') 


    def test_category(self):
        u_id2 = models.createUser({'username':'user2',
                                     'email':'user2@email.com'})
        cat_id = models.addCategory(name='category1', user_id=u_id2,
                             description='This is category1')
        print("category_id: %s" %(cat_id))
        c1 = models.getCategory(cat_id)
        print "c1.name: " + c1.name
        pprint.pprint(c1.serialize)
        self.assertEqual(c1.category_id, cat_id)
        self.assertEqual(c1.name, 'category1')
        self.assertEqual(c1.user_id, u_id2)
        self.assertEqual(c1.description, 'This is category1')

        # create Category object without description	
        id2 = models.addCategory(name='category2', user_id=u_id2)
        c2 = models.getCategory(id2)
        self.assertEqual(c2.name, 'category2')
        self.assertEqual(c2.user_id, u_id2)
        self.assertEqual(c2.description, None)

        # delete Category
        models.deleteCategory(id2)
        c2 = models.getCategory(id2)
        self.assertEqual(c2, None)


    def test_item(self):
        u_id3 = models.createUser({'username':'user3',
                                     'email':'user3@email.com'})

        c_id = models.addCategory(name='cat1', user_id=u_id3)

        i_id1 = models.addItem(name='item1', user_id=u_id3,
                             category_id=c_id,
                            description='This is item1')
        item1 = models.getItem(i_id1)
        self.assertEqual(item1.item_id, i_id1)
        self.assertEqual(item1.name, 'item1')
        self.assertEqual(item1.user_id, u_id3)
        self.assertEqual(item1.category_id, c_id)
        self.assertEqual(item1.description, 'This is item1')

        # without description
        i_id2 = models.addItem(name='item2', user_id=u_id3,
                               category_id=c_id)

        # delete item
        models.deleteItem(i_id2)
        item2 = models.getItem(i_id2)
        assertEqual(item2, None)


if __name__ == '__main__':
    unittest.main()
