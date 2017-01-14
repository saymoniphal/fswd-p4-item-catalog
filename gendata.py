#!/usr/bin/env python

import random
import sys

from sqlalchemy import create_engine

import config
import models


def main(username):
    engine = create_engine(config.DB_URI)
    models.Base.metadata.create_all(engine)

    sess = models.connect_db(config.DB_URI)
    user = models.User.getByName(sess, username)
    for i in range(64):
        cat = models.Category(name='cat ' + str(i),
                              description='This is category ' + str(i),
                              user=user)
        for j in range(random.randint(100, 200)):
            it = models.Item(name='item ' + str(i) + ',' + str(j),
                             description='This is item ' + str(j) +
                             ' in category ' + str(i),
                             category=cat)
            cat.items.append(it)
        user.categories.append(cat)
    sess.commit()

if __name__ == '__main__':
    main(sys.argv[1])
