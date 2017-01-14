apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-requests python-oauth2client
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb catalog'
su vagrant -c 'python /vagrant/dbsetup.py'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant[m"
echo -e $vagrantTip > /etc/motd
