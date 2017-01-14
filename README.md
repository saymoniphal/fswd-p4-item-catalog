# Project Overview

The catalog app provides a web interface to create and maintain an
item catalog.  Multiple categories can be created to organize the
catalog, and items can be assigned particular categories.

## How to get source code

Use Git or checkout with SVN using the web url:
`https://github.com/saymoniphal/fswd-p4-item-catalog.git`

## How to run project

This project requires PostgreSQL database, you may run it on the
system with PostgreSQL server installed or use Vagrant virtual
machine.

Either way, you should modify the `config.py` file and change
`SECRET_KEY` to some random string for your instance.  Any value is
fine, as long as you have generated it yourself and don't share it
with other instances.

Additionally, you should modify the `catalog/client_secrets.json` file
and provide your own configuration information for authenticating
users with Google.

### Use Vagrant virtual machine

1. Go to `catalog` directory in the terminal.

2. Run the `vagrant up` command.  This creates the required virtual
   machine, installs the required packages and creates the catalog
   database.

3. Run `vagrant ssh -- python /vagrant/run.py` to start the
   application server

4. Open any web browser and type `http://localhost:5000` to view the
   catalog

### Run without vagrant

1. Ensure the `python-psycopg2` library is installed.

2. Create a database for use by the item catalog.

3. Edit `config.py` and point `DB_URI` to the URI of the database the
   catalog should use.

4. Run `python dbsetup.py` to create required tables.

5. Run `python run.py` to run the app.

6. Open any web browser and type `http://localhost:5000` to view the
   catalog

## Project structure

The item catalog uses PostgreSQL as the database.  If you want to use
it with a different database, make sure you have the required python
libraries installed, and update the `DB_URI` entry in the `config.py`
file to contain a URI suitable for sqlalchemy.  Refer to the
sqlalchemy docs for details on the URI format.

If you are a developer, the following files might be useful if you
want to work on fixing bugs or adding features to the application:

- `pg_config.sh`, `Vagrantfile`: These files configure vagrant VM and
  install required packages inside it.

- `config.py`: This file contains configuration information.

- `dbsetup.py`: Run this script to create tables in the configured
  database.

- `gendata.py`: Run this script with a username to create several
  categories and items to test the web interface.

- `db_test.py`: Contains unittests for the model.

- `run.py`: Run this script to start the webserver serving the catalog
  app.

- `catalog/views`: This directory contains various jinja2 templates.
  Modify these if you want to change how the web interface looks and
  behaves.

- `catalog/static`: This directory contains various statically served
  files, such as css files and javascript code.

# Licenses

This project uses code from the following projects:

## Bootstrap

The MIT License (MIT)

Copyright (c) 2011-2016 Twitter, Inc.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
