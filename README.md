## Project Overview
This goal of project is to built a database schema and python program to keep
track of players and matches in a game tournament using swiss-paring system.
This supports multiple tournaments.

## How to get source code
Use Git or checkout with SVN using the web url:
https://github.com/saymoniphal/fswd3-tournament-result.git

## How to run project
This project requires PosgreSQL database, you may run it on the system with
PosgreSQL server installed or use Vagrant virtual machine.

#### Use Vagrant virtual machine

1. Go to ```catalogue``` directory in the terminal,
Run command ```vagrant up``` (powers on the virtual machine),
Run command ```vagrant ssh``` (logs into the virtual machine),
2. run ```python dbset.py``` to create the tables in the database,
this needs to run once only.
3. run ```python run.py``` to start the application server
4. Open any web browser and type ```http://localhost:5000``` to view the catalogue

Example:

```
moniphal@titanium:~/git-trees/vagrant/fswd-p3-tournament-result$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'ubuntu/trusty32'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'ubuntu/trusty32' is up to date...
==> default: A newer version of the box 'ubuntu/trusty32' is available! You currently
==> default: have version '20161109.0.0'. The latest is version '20161122.0.0'. Run
==> default: `vagrant box update` to update.
==> default: Setting the name of the VM: fswd-p3-tournament-result_default_1480499539203_97178
==> default: Clearing any previously set forwarded ports...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
...
...
```

```

moniphal@titanium:~/git-trees/vagrant/fswd-p3-tournament-result$ vagrant ssh
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 3.13.0-101-generic i686)

 * Documentation:  https://help.ubuntu.com/

 System information disabled due to load higher than 1.0

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

0 packages can be updated.
0 updates are security updates.

New release '16.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

The shared directory is located at /vagrant
To access your shared files: cd /vagrant
Last login: Wed Nov 30 10:03:24 2016 from 10.0.2.2

```

```
vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/
vagrant@vagrant-ubuntu-trusty-32:/vagrant$ ls
config.py  database.ini  pg_config.sh  README.md  tournament.py  tournament.sql  tournament_test.py  Vagrantfile

vagrant@@vagrant-ubuntu-trusty-32:/vagrant$ ls
config.py  database.ini  README.md  tournament.py  tournament.sql  tournament_test.py


## Project structure
The database used in this project is Postgresql.

The project structure is as below:
<pre>
|-- README.md
|-- tournament.sql: setup database schema (database and tables definitions ) 
|-- tournament.py: provides access to the database to add, delete, query data
|-- tournament\_test.py: provides unit tests for the funtionality implemented
in tournament.py
|-- database.ini: contains database configuration (database name)
|-- config.py: provides access to database.ini file.

|-- pg_config.sh and Vagrantfile: these files are taken from
http://github.com/udacity/fullstack-nanodegree-vm as part of Udacity course.
</pre>
