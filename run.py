#!/bin/bash/env python

from catalog import app


def main():
    app.secret_key = app.config['SECRET_KEY']
    app.db_uri = app.config['DB_URI']
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
