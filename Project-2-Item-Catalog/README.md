# Item Catalog Web App

This web app is a project for the Udacity FSND Course.

## About Project

This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit, and delete their own items.

## Features

- Full CRUD support using SQLAlchemy and Flask.
- Proper authentication and authorisation check.
- JSON endpoints.
- Implements oAuth using Google Sign-in API.
  
## Structure Details

This project has one main Python module application.py which runs the Flask application. A SQL database is created using the database_setup.py module and you can populate the database with test data using data_addition.py. The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. CSS and HTML templates are stored in the static directory.

## Running Environment

- Python: 2.7.12
- PostgreSQL: 9.5.8
- Flask: 1.0.3
- Vagrant: 2.3.5
- Virtualbox: 6.0

## Steps to run this project

1. Setup Project
    1. Download and install the virtual box.
    Download virtual box from following link:
    [Download Virtual box] (https://www.virtualbox.org/wiki/Downloads)
    2. Download and install Vagrant VM from following link:
    [Download Vagrant] (https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)

2. Set up the VM
    1. From your bash terminal, move to the same directory where this Vagrant file is located and run the following command to start VM:
    $ vagrant up
    2. Then Log in to VM this using command:
    $ vagrant ssh
    3. Now change directory to /vagrant and go to project folder.

3. Setting up the project and database:
   1. Set up the project database by using command:
    $ python database_setup.py
   2. Load the data in database by using the command:
    $ python data_addition.py

4. Run the application:
    $ python application.py

## JSON Endpoints

The following are open to the public:

Catalog JSON: /catalog/JSON - Displays the whole catalog with all categories and items.

Categories JSON: /catalog/categories/JSON - Displays all categories

Items JSON: /catalog/items/JSON: Displays all the items.

Category Items JSON: /catalog/'category name'/items/JSON - Displays all the items for a specific category.

Item JSON: / catalog/'category name'/'item name'/JSON - Displays details for a specific item.
