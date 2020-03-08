from app.api import bp
from flask import jsonify, request
from app.models import Restaurant, Menu, Table
from flask import url_for
from app import db
from app.api.errors import bad_request

@bp.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def restaurant(id):
    #""" Get a restaurant. """    
    if request.method == 'GET':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')
        response = jsonify(restaurant.to_dict())
        response.headers['Location'] = url_for('api.restaurant', id=id)
        return response

    #""" Update restaurant's details. """
    elif request.method == 'PUT':
        response = jsonify({"status": 'restaurant details updated'})
        return response

    #""" Delete a restaurant. """
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')
        data = restaurant.to_dict()
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({"status": 'restaurant deleted'})

    #""" POST method not allowed on this endpoint. """
    elif request.method == 'POST':
        return bad_request("You cannot create restauarnt on this end point. Use this for a POST request: "+ url_for('api.restaurants'))

    else:
        return bad_request("That's a bad request.")

@bp.route('/restaurants', methods=['GET', 'POST', 'PUT', 'DELETE'])
def restaurants():
    #""" Get All Restaurants. """
    if request.method == 'GET':
        restaurants = Restaurant.query.all()
        response = jsonify(
                        {'restaurants': [restaurant.to_dict() for restaurant in restaurants],
                        '_link': url_for('api.restaurants')
                        }
            )
        response.headers['Location'] = url_for('api.restaurants')
        return response

    #""" Create a restaurant. """
    elif request.method == 'POST':
        data = request.get_json() or {}

        if 'name' not in data and 'email' not in data and 'contact' not in data:
            return bad_request('Restaurant name, email and contact was missing from the request.')
        if 'name' not in data:
            return bad_request('Restaurant name was missing from the request.')
        if 'email' not in data:
            return bad_request('Email was missing from the request.')
        if 'contact' not in data:
            return bad_request('Contact was missing from the request.')            
        if Restaurant.query.filter_by(name=data['name']).first():
            return bad_request('This Restaurant name is already registered.')
        if Restaurant.query.filter_by(email=data['email']).first():
            return bad_request('This email is already in use by another restuarant. Please use a different email.')

        restaurant = Restaurant()
        restaurant.from_dict(data)

        db.session.add(restaurant)
        db.session.commit()
        response = jsonify(restaurant.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.restaurant', id=restaurant.id)
        return response

    #""" PUT method not allowed on this endpoint. """
    elif request.method == 'PUT':
        return bad_request("You cannot update a restaurant on this end point. Use this for a PUT request with an id: "+ url_for('api.restaurant')+"/<id>")

    #""" DELETE method not allowed on this endpoint. """
    elif request.method == 'DELETE':
        return bad_request("You cannot delete a restaurant on this end point. Use this for a DELETE request with an id: "+ url_for('api.restaurant')+"/<id>")

    else:
        return bad_request("That's a bad request.")


@bp.route('/restaurants/<int:id>/menus/<int:menu_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def menu(id, menu_id):
    #""" Get a particular menu of a restaurant. """    
    if request.method == 'GET':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        menu = Menu.query.get(menu_id)
        if menu is None:
            return bad_request('Menu id is not correct.')
        else:
            response = jsonify(menu.to_dict())
            response.headers['Location'] = url_for('api.menu', id=id, menu_id=menu_id)
            return response

    #""" Update a particular menu of a restaurant.. """
    elif request.method == 'PUT':
        response = jsonify({"status": 'menu details updated'})
        return response

    #""" Delete a particular menu for a restaurant. """
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        menu = Menu.query.get(menu_id)
        if menu is None:
            return bad_request('Menu id is not correct.')

        data = menu.to_dict()
        db.session.delete(menu)
        db.session.commit()
        return jsonify({"status": 'menu deleted'})

    #""" POST method not allowed on this endpoint. """
    elif request.method == 'POST':
        return bad_request("You cannot create menus on this end point. Use this for a POST request: "+ url_for('api.menus', id=id))

    else:
        return bad_request("That's a bad request.")


@bp.route('/restaurants/<int:id>/menus', methods=['GET', 'POST', 'PUT', 'DELETE'])
def menus(id):
    #""" Get All Menus for a Restaurant. """
    if request.method == 'GET':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        menus = Menu.query.filter_by(owner=restaurant).all()

        if menus is None or menus==[]:
            return bad_request('Menu id is not correct.')
        else:      
            response = jsonify(
                            {'menus': [menu.to_dict() for menu in menus],
                            '_link': url_for('api.menus', id=restaurant.id)
                            }
                )
            response.headers['Location'] = url_for('api.menus', id=restaurant.id)
            return response

    #""" Create a Menu for a restaurant. """
    elif request.method == 'POST':
        data = request.get_json() or {}

        if 'name' not in data:
            return bad_request('Restaurant name was missing from the request.')
        else:
            restaurant =  Restaurant.query.filter_by(name=data['name']).first()
            if restaurant is None:
                return bad_request('Restaurant id is not correct.')

        if 'description' not in data:
            return bad_request('Menu Description was missing from the request.')
        if 'menu_type' not in data:
            return bad_request('Menu Type was missing from the request.')            
        if Menu.query.filter_by(owner=restaurant, description=data['description']).first():
            return bad_request('This Menu is already created for this restuarant.')

        menu = Menu()
        menu.from_dict(data)

        if menu.restaurant_id == 0:
            return bad_request('Restaurant id is not correct.')

        db.session.add(menu)
        db.session.commit()
        response = jsonify(menu.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.menu', id=menu.owner.id, menu_id=menu.id)
        return response

    #""" PUT method not allowed on this endpoint. """
    elif request.method == 'PUT':
        return bad_request("You cannot update a menu on this end point. Use this for a PUT request with a menu_id: "+ url_for('api.restaurant', id=id) + "/menus/<menu_id>")

    #""" DELETE method not allowed on this endpoint. """
    elif request.method == 'DELETE':
        return bad_request("You cannot delete a menu on this end point. Use this for a DELETE request with a menu_id: "+ url_for('api.restaurant', id=id) + "/menus/<menu_id>")

    else:
        return bad_request("That's a bad request.")


@bp.route('/restaurants/<int:id>/tables/<int:table_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def table(id, table_id):
    #""" Get a particular Table of a restaurant. """    
    if request.method == 'GET':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        res_table = Table.query.get(table_id)

        if res_table is None:
            return bad_request('Table id is not correct.')
        elif res_table.restaurant_id != restaurant.id:
            return bad_request('Restaurant/Table id combination is not correct.')
        else:
            response = jsonify(res_table.to_dict())
            response.headers['Location'] = url_for('api.table', id=id, table_id=table_id)
            return response

    #""" Update a particular Table of a restaurant.. """
    elif request.method == 'PUT':
        response = jsonify({"status": 'menu details updated'})
        return response

    #""" Delete a Table for a restaurant. """
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        res_table = Table.query.get(table_id)
        if res_table is None:
            return bad_request('Table id is not correct.')

        data = res_table.to_dict()
        db.session.delete(res_table)
        db.session.commit()
        return jsonify({"status": 'table deleted'})

    #""" POST method not allowed on this endpoint. """
    elif request.method == 'POST':
        return bad_request("You cannot create tables on this end point. Use this for a POST request: "+ url_for('api.tables', id=id))

    else:
        return bad_request("That's a bad request.")


@bp.route('/restaurants/<int:id>/tables', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tables(id):
    #""" Get All Tables for a Restaurant. """
    if request.method == 'GET':
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return bad_request('Restaurant id is not correct.')

        res_tables = Table.query.filter_by(owner=restaurant).all()
        
        if res_tables is None or res_tables==[]:
            return bad_request('Table id is not correct.')
        else:      
            response = jsonify(
                            {'tables': [res_table.to_dict() for res_table in res_tables],
                            '_link': url_for('api.tables', id=restaurant.id)
                            }
                )
            response.headers['Location'] = url_for('api.tables', id=restaurant.id)
            return response

    #""" Create a Table for a restaurant. """
    elif request.method == 'POST':
        data = request.get_json() or {}

        if 'name' not in data:
            return bad_request('Restaurant name was missing from the request.')
        else:
            restaurant =  Restaurant.query.filter_by(name=data['name']).first()
            if restaurant is None:
                return bad_request('Restaurant id is not correct.')

        if 'number' not in data:
            return bad_request('Table number was missing from the request.')
        if 'capacity' not in data:
            return bad_request('Capacity for Table was missing from the request.')            
        if Table.query.filter_by(owner=restaurant, number=data['number']).first():
            return bad_request('This Table is already created for this restuarant.')

        res_table = Table()
        res_table.from_dict(data)

        if res_table.restaurant_id == 0:
            return bad_request('Restaurant Id is not correct.')

        db.session.add(res_table)
        db.session.commit()
        response = jsonify(res_table.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.table', id=res_table.owner.id, table_id=res_table.id)
        return response


    #""" PUT method not allowed on this endpoint. """
    elif request.method == 'PUT':
        return bad_request("You cannot update a table on this end point. Use this for a PUT request with a table_id: "+ url_for('api.restaurant', id=id) +"/tables/<table_id>")

    #""" DELETE method not allowed on this endpoint. """
    elif request.method == 'DELETE':
        return bad_request("You cannot delete a table on this end point. Use this for a DELETE request with a table_id: "+ url_for('api.restaurant', id=id) + "/tables/<table_id>")

    else:
        return bad_request("That's a bad request.")