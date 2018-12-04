import random
import string
import json
import requests
import httplib2
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, Category, Item, User





app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    """Show the login webpage for creating and editing items
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Use Google to authenticate and login into the application
    """
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
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
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
    login_session['provider'] = 'google'

    # check if the user exists
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: \
                  150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    """ Create a user in the User database
        login_session: Flask user login_session object

        Returns:
        user.id: user_id in the database
    """
    session = DBSession()
    newuser = User(name=login_session['username'], email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newuser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Get user from database
       user_id: database user id

       Returns:
       user: database entry
    """
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Get database user_id
       email: user's email

       Returns:
       user.id: user_id in the database
    """
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnect a user that logged in with a Google account
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    return response


# JSON APIs to view Categories
@app.route('/categories/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    """Get all items in a category in json format
       category_id: Database id of the category

       Returns:
       json object
    """
    session = DBSession()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/item/<int:item_id>/JSON')
def ItemJSON(item_id):
    """Get an item in json format
       item_id: Database id of the item

       Returns:
       json object
    """
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


@app.route('/categories/JSON')
def categoriesJSON():
    """Get all categories in json format
       category_id: Database id of the category

       Returns:
       json object
    """
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/')
@app.route('/categories/')
def showCategories():
    """Show all categories on a webpage
    """
    session = DBSession()
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).limit(5)
    return render_template('catalog.html', categories=categories, items=items)


@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    """Show the items of a single category on a webpage
    """
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('items.html', items=items, category=category)


@app.route('/item/<int:item_id>/')
def showSingleItem(item_id):
    """Show a single item on a webpage
    """
    session = DBSession()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('showitem.html', item=item)


@app.route('/item/new/', methods=['GET', 'POST'])
def newItem():
    """Create a new item in the database using a webpage form
    """
    session = DBSession()
    # Check if the user is authenticated
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if not request.form['name'] or not request.form['description'] or not request.form['category']:
            return render_template('newitem.html')
        category = session.query(Category).filter_by(name=request.form['category']).one()
        itemnew = Item(name=request.form['name'], description=request.form['description'],
                       category_id=category.id, user_id=login_session['user_id'])
        session.add(itemnew)
        session.commit()
        flash('New Menu %s Item Successfully Created' % itemnew.name)
        return redirect(url_for('showSingleItem', item_id=itemnew.id))
    else:
        return render_template('newitem.html')


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(item_id):
    """Edit an item in the database using a webpage form
    """
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editeditem = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != editeditem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit  this item. Please create your \
                own items in order to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        if request.form['description']:
            editeditem.description = request.form['description']
        session.add(editeditem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showSingleItem', item_id=editeditem.id))
    else:
        return render_template('edititem.html', item=editeditem)


@app.route('/item/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    """Delte an item from the database using a webpage form
    """
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    itemtodelete = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != itemtodelete.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your \
                own items in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteitem.html', item=itemtodelete)


@app.route('/disconnect')
def disconnect():
    """Disconnect an user from the application by freeing resources in the login_session
    flask object
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCategories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
