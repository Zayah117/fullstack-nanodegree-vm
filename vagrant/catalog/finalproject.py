from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__, static_url_path='/static/*')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/restaurants/JSON')
def restauranstJSON():
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    items = session.query(Restaurant).all()
    return render_template('restaurants.html', items=items)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newItem = Restaurant(name = request.form['name'])
        session.add(newItem)
        session.commit()
        flash("new restaurant created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        newEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
        newEdit.name = request.form['edit']
        session.add(newEdit)
        session.commit()
        flash("restaurant edited")
        return redirect(url_for('showRestaurants'))
    else:
        item = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('editrestaurant.html', restaurant_id=restaurant_id, item=item)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        item = session.query(Restaurant).filter_by(id=restaurant_id).one()
        session.delete(item)
        session.commit()
        flash("restaurant deleted")
        return redirect(url_for('showRestaurants'))
    else:
        item = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('deleterestaurant.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id=restaurant_id)
        newItem.description = request.form['description']
        newItem.price = request.form['price']
        newItem.course = request.form['course']
        session.add(newItem)
        session.commit()
        flash("new menu item created.")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        newEdit = session.query(MenuItem).filter_by(id=menu_id).one()
        newEdit.name = request.form['edit']
        newEdit.description = request.form['description']
        newEdit.price = request.form['price']
        newEdit.course = request.form['course']
        session.add(newEdit)
        session.commit()
        flash("menu item edited.")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(item)
        session.commit()
        flash("menu item deleted.")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)