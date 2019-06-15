#!/usr/bin/python

import sys
import os
from flask import Flask
from flask import request, redirect, url_for, render_template, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

# Imports for login
from flask import session as login_session
import random
import string
from functools import wraps

# IMPORTS FOR GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Flask instance
app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item Application"

#  Connect to database
engine = create_engine('sqlite:///catalog_items.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

# Create session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
# return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# gconnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match with\
                        given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match with app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is\
                                            already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

# Check if a user exists, if it doesn't then make a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
                           border-radius: 150px;-webkit-border-radius: 150px;\
                           -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        import platform_specific_module
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except ImportError:
        platform_specific_module = None
        return None


# gdisconnect
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'
                                            ), 401)
        response.headers['Content-Type'] = 'application/json'
# return response
    url = 'https://accounts.google.com/o/oauth2/revoke?\
           token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps('Failed to revoke token \
                                 for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showCatalog'))


# login required
# def login_required(f):
# Flask Routing
# Home Page
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('catalog.html', categories=categories, items=items)


# Show Category
@app.route('/catalog/<path:category_name>')
def showCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    return render_template('category.html', category=category)


# Show Category Item
@app.route('/catalog/<path:category_name>/Items')
def showCategoryItem(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    items = session.query(Item).all()
    return render_template('categoryItem.html', category=category, items=items)


# Show Item Description
@app.route('/catalog/<path:category_name>/<path:item_name>')
def showItemDescription(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).first()
    item = session.query(Item).filter_by(name=item_name).first()
    return render_template('item.html', category=category, item=item)


# Add a new Category
@app.route('/catalog/addCategory', methods=['GET', 'POST'])
# @login_required
def addCategory():
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    categories = session.query(Category).all()

    if request.method == 'POST':

        # Check if category already exists
        category = session.query(Category).\
        filter_by(name=request.form['name']).first()
        
        if category is not None:
            flash('The entered category already exists.')
            return redirect(url_for('addCategory'))

        # Adds new category
        newCategory = Category(name=request.form['name'],\
                            user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('New Category successfully added')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addCategory.html', categories=categories)


# Edit a Category
@app.route('/catalog/<path:category_name>/editCategory',
           methods=['GET', 'POST'])
# @login_required
def editCategory(category_name):
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).first()

    # See if the logged in user is the owner of item
    creator = getUserInfo(category.user_id)
    
    # If logged in user != category owner then redirect them
    if creator.id != login_session['user_id']:
        flash("You are not authorised to edit this category.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
            session.add(category)
            session.commit()
            flash("Category successfully edited!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editCategory.html', category=category)


# Delete a Category
@app.route('/catalog/<path:category_name>/deleteCategory',
           methods=['GET', 'POST'])
# @login_required
def deleteCategory(category_name):
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    categoryToDelete = session.query(Category).filter_by\
    (name=category_name).first()

    # See if the logged in user is the owner of item
    creator = getUserInfo(categoryToDelete.user_id)

    # If logged in user != category owner then redirect them
    if creator.id != login_session['user_id']:
        flash("You are not authorised to delete this category.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        flash("Category successfullt deleted!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete)


# Add a new Item
@app.route('/catalog/addItem', methods=['GET', 'POST'])
# @login_required
def addItem():
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id']
            )
        session.add(newItem)
        session.commit()
        flash('New item successfully added')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('addItem.html', categories=categories)


# Edit an Item
@app.route('/catalog/<path:category_name>/<path:item_name>/editItem',
           methods=['GET', 'POST'])
# @login_required
def editItem(category_name, item_name):
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    editedItem = session.query(Item).filter_by(name=item_name).first()
    category = session.query(Category).filter_by(name=category_name).first()

    # See if the logged in user is the owner of item
    creator = getUserInfo(editedItem.user_id)

    # If logged in user != category owner then redirect them
    if creator.id != login_session['user_id']:
        flash("You are not authorised to edit this item.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash("Item successfully edited!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('editItem.html', category_name=category,
                               item=editedItem)


# Delete an Item
@app.route('/catalog/<path:item_name>/deleteItem', methods=['GET', 'POST'])
# @login_required
def deleteItem(item_name):
    # Check if User is logged in
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect('/login')

    itemToDelete = session.query(Item).filter_by(name=item_name).one_or_none()

    # Check for the authority
    #if login_session['user_id'] != itemToDelete.user_id:
    #    flash("You are not authorised to delete this item.")
    #    return redirect(url_for('showCatalog'))

    # See if the logged in user is the owner of item
    creator = getUserInfo(itemToDelete.user_id)

    # If logged in user != category owner then redirect them
    if creator.id != login_session['user_id']:
        flash("You are not authorised to delete this item.")
        return redirect(url_for('showCatalog'))

    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item successfullt deleted!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# Adding JSON API Endpoint
@app.route('/catalog/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(categories=[c.serialize for c in categories],
                   items=[i.serialize for i in items])


@app.route('/catalog/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/catalog/items/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<path:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<path:category_name>/<path:item_name>/JSON')
def itemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,
                                         category=category).one()
    return jsonify(item=[item.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
