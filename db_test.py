import os
import unittest
import pprint

import models


class TestDBConnection(unittest.TestCase):

    def setUp(self):
        self.session = models.connect_db('sqlite:////tmp/itemcatalog.db')
        models.Base.metadata.create_all(self.session.bind)

    def tearDown(self):
        self.session.close()
        os.unlink('/tmp/itemcatalog.db')

    def test_user(self):
        user1 = models.User.create(self.session, 'user1', 'user1@email.com')
        self.session.commit()
        self.assertEqual(user1.name, 'user1')
        self.assertEqual(user1.email, 'user1@email.com') 


    def test_category(self):
        user1 = models.User.create(self.session, 'user2', 'user2@email.com')
        cat1 = models.Category.create(self.session, 'category1', user1, 'This is category1')
        self.assertEqual(cat1.name, 'category1')
        self.assertEqual(cat1.description, 'This is category1')

        # create Category object without description	
        cat2 = models.Category.create(self.session, 'category2', user1)
        self.assertEqual(cat2.name, 'category2')
        self.assertEqual(cat2.description, None)

        self.session.commit()

        self.assertEqual(user1.categories, [cat1, cat2])

        # delete Category
        self.session.delete(cat2)

    def test_item(self):
        user1 = models.User.create(self.session, 'user3', 'user3@email.com')
        cat1 = models.Category.create(self.session, 'cat1', user1)
        item1 = models.Item.create(self.session, 'item1', cat1, 'This is item1')
        self.assertEqual(item1.name, 'item1')
        self.assertEqual(item1.description, 'This is item1')

        # without description
        item2 = models.Item.create(self.session, 'item2', cat1)
        self.assertEqual(item2.name, 'item2')
        self.assertEqual(item2.description, None)

        self.session.commit()
        self.assertEqual(user1.categories[0].items, [item1, item2])

        # delete item
        self.session.delete(item2)


if __name__ == '__main__':
    unittest.main()
