# Linux Server Configuration

Objective of this project is to configure linux virtual machine to support Sport catalog web application. Document explains steps required to complete installation of updates, securing the system from a number of attack vectors and installing/configuring web and database servers.

Project is developed as part of Udacity's Full Stack Web Developer Nanodegree courses Configuring Linux Web Servers.

## Server Information

- Public IP Address: (http://52.221.180.192/)
- Virtual Server: Amazon Lightsail Instance
- Operating System: Ubuntu 16.04 LTS
- SSH Port: 2200 (Only Key based logins supported)
- Web Server: Apache2 Web Server

## Software Installed

- Git 2.7.4
- Python: 2.7.12
- PostgreSQL: 9.5.8
- Flask: 1.0.3
- SQLAlchemy 1.3.4
- bleach 3.1.0
- google-auth 1.6.2
- psycopg2-binary 2.8.3
- requests 2.22.0

## Steps to deply the project on server

1. [Prepare the remote server](#Prepare the REMOTE SERVER)
2. [Configure the Firewall] (# Configure firewall to allow SSH, port 80, 123 and 2200 )
3. [Create the User - grader] (# User Creation)
4. [Generate the SSH Keypair and set-up](# Generate SSH Keypairs for users)
5. [SSH Configurations] (# SSH Configurations)
6. [Software package installation] (# Package Installation)
7. [PostgreSQL configuration] (# PostgreSql Congigurations)
8. [Set up the project] (# Clone and setup Catalog App project)
9. [Enable the virtual host to run the project] (# Configure and Enable a New Virtual Host)
10. [Restart the server and run the project] (# Restart Apache)

### Prepare the REMOTE SERVER

- Login to the server as user ubuntu using ssh connection

- Update the operating system pakages and reboot if required

```sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo reboot
```

- Configure automatic security and critical updates
Follow the official documentation:
[Ubuntu Automatic Update Configuration] (https://help.ubuntu.com/lts/serverguide/automatic-updates.html.en)

- Set timezone to UTC

- Check if the current timezone is set to UTC using:

`$ date`

- If not UTC set timezone to UTC using the command below:

`sudo dpkg-reconfigure tzdata`

select 'None of the above' from the menu and then select 'UTC'.

### Configure firewall to allow SSH, port 80, 123 and 2200

- Set UFW defaults:

```sudo ufw default deny incoming
sudo ufw default allow outgoing
```

- Allow connections for SSH (port 2200), HTTP (port 80), and UDP (port 123):

```sudo ufw allow 2200
sudo ufw allow 80
sudo ufw allow 123
```

- Deny the port 22

`sudo ufw deny 22`

- Enable Firewall:

`sudo ufw enable`

- Check firewall status

`sudo ufw status`

### User Creation

- Create user 'grader'

`sudo adduser grader`

- Add user into sudoers list

`sudo cp /etc/sudoers.d /etc/sudoers.d/grader`

- Edit the sudoers.d file

`sudo nano /etc/sudoers.d/grader`

- Add the following line into file

`grader ALL=(ALL:ALL) ALL`

- Try to run the command

`sudo cat /etc/passwd`

Should display the content

### Generate SSH Keypairs for user

- Connect to REMOTE MACHINE using the ubuntu user

```su - grader
mkdir .ssh
touch .ssh/authorized_keys
nano .ssh/authorized_keys
```

- Now go to LOCAL TERMINAL and generate ssh keypair

`ssh-keygen`

This command will generate 2 files, public key `fsnd_linux.pub` and private key `fsnd_linux.rsa`.

- Save these files in .ssh folder
- Now open the .pub file and copy the whole file content.
- Go to the previously opened terminal (on REMOTE MACHINE)
- Paste the .pub content in the file (in authorized_key file)
- Save the file and close it

- On REMOTE machine, perform the following commands to give all permissions (as a ubuntu user)

```chmod 700 .ssh
chmod 644 .ssh/authorized_keys
```

- On LOCAL machine, use the PRIVATE key `fsnd_linux.rsa` (created with ssh-keygen command) to connect to REMOTE MACHINE

`ssh grader@52.221.180.192 -p 2200 -i ~/FSND-Project-Linux-Server/.ssh/fsnd_linux`

### SSH Configurations

- Run the following command

`sudo nano /etc/ssh/sshd_config`

- Change the SSH default port by locating the following line and change 22 to 2200:

```# What ports, IPs and protocols we listen for
Port 2200
```

- Remove root login by locating the following line and change without-password to no:

```# Authentication:
PermitRootLogin without-password (or no)
```

- Force SSH login by locating the following line and change yes to no:

```# Change to no to disable tunnelled clear text passwords
PasswordAuthentication no
```

- Restart the ssh service for the changes to take effect:

`sudo service ssh restart`

Now key based login is enforced

### Software Package Installation

- Install apache2 package:

`sudo apt-get install apache2`

- Install mod_wsgi package:

`sudo apt-get install libapache2-mod-wsgi`

- Install postgresql package:

`sudo apt-get install postgresql`

- Install git package:

`sudo apt-get install git`

- Install python packages:

```sudo apt-get -qqy install python python-pip
 sudo pip2 install --upgrade pip
 sudo pip2 install flask packaging oauth2client redis passlib flask-httpauth
 sudo pip2 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests
 sudo apt-get install python-oauth2client
 sudo apt-get install python-httplib2
 sudo apt-get install python-psycopg2 python-flask
 sudo apt-get install python-sqlalchemy python-pip
```

- Upgrade and update all software packages

```sudo apt-get update
sudo apt-get dist-upgrade
```

### PostgreSql Congigurations and Database creation

- Ensure access method is updated from peer to md5.

`sudo nano /etc/postgresql/9.5/main/pg_hba.conf`

- Restart postgres server
  
`sudo service postgresql restart`

- Login as user postgres into shell
  
`sudo su - postgres psql`

#### Create a new database named catalog by using postgreSQL shell:

`postgres=# CREATE DATABASE catalog;`

- Create a new user named catalog

`postgres=# CREATE USER catalog;`

- Set a password for user catalog:

`postgres=# ALTER ROLE userdb WITH PASSWORD 'catalog';`

- Give user "catalog" permission to "catalog" database:

```postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
postgres=# GRANT ALL ON SCHEMA PUBLIC to catalog;
postgres=# REVOKE ALL ON SCHEMA PUBLIC FROM PUBLIC;
```

- Quit and exit postgreSQL:

`postgres=# \q`
`exit`

### Clone and setup 'Item Catalog App' project files

- Move to /var/www directory
  
 `cd /var/www`

- Create the application directory

`sudo mkdir FlaskApp`

- Move inside the directory FlaskApp and clone the project repository

`git clone (https://github.com/UnnatiSangani/Udacity-FSND-Projects)`

- Rename the project's name and ensure all files are under directory /var/www/FlaskApp. Remove unwwanted files

`sudo mv ./Project-2-Item-Catalog ./FlaskApp`

- Changing permissions of files

`sudo chmod -R 777 *`

- Move to the inner FlaskApp directory

- Rename application.py to __init__.py using

`sudo mv application.py __init__.py`

- Edit database_setup.py, data_addition.py files and change the following line to change the engine

```engine = create_engine('sqlite:///items_catalog.db') to
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
```

- Create database schema

`sudo python database_setup.py`

### Configure and enable a new Virtual Host

- Create FlaskApp.conf to edit:

`sudo nano /etc/apache2/sites-available/FlaskApp.conf`

- Add the following lines of code to the file to configure the virtual host:

```<VirtualHost *:80>
        ServerName itemcatalog.com
        ServerAlias www.itemcatalog.com
        ServerAdmin a.unnati@gmail.com
        DocumentRoot /var/www/FlaskApp
        WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
        <Directory /var/www/FlaskApp/>
                Order allow,deny
                Allow from all
        </Directory>
        Alias /static /var/www/FlaskApp/static
        <Directory /var/www/FlaskApp/static/>
                Order allow,deny
                Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

- Enable the virtual host:

`sudo a2ensite FlaskApp.conf`

- Disable default host:

`sudo a2dissite 000-default.conf`

#### Create the .wsgi File

- Create the .wsgi File under /var/www/FlaskApp:

```cd /var/www/FlaskApp
sudo vi flaskapp.wsgi
```

- Add the following lines of code to the flaskapp.wsgi file:

```#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
```

### Restart Apache

`sudo service apache2 restart`

### References

- (https://www.thegeekstuff.com/2009/04/linux-postgresql-install-and-configure-from-source/)
- (https://help.ubuntu.com/lts/serverguide/automatic-updates.html.en)
- (https://help.ubuntu.com/community/SSH/OpenSSH/Keys)
- (https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
