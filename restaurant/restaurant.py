from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###################################
##########  RESTAURANTS  ##########
###################################
class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    rest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=False)
    address = db.Column(db.String(300), nullable=False)
    
    def __init__(self, name, is_open, address):
        self.name = name
        self.is_open = is_open
        self.address = address

    def json(self):
        return {
            "name": self.name,
            "is_open": self.is_open,
            "address": self.address
        }
        
@app.route("/restaurant")
def get_all_restaurant():
    restaurantlist = Restaurant.query.all()
    if len(restaurantlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "restaurants": [restaurant.json() for restaurant in restaurantlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no restaurants."
        }
    ), 404

@app.route("/restaurant/<rest_id>", methods=['GET'])
def get_restaurant(rest_id):
    restaurant = Restaurant.query.filter_by(rest_id=rest_id).first()
    # orderStatus = OrderStatus.query.filter_by(order_id=order_id).first()

    if restaurant is None:
        return jsonify(
            {
                "status": "error",
                "message": "Restaurant of id {0} does not exists".format(rest_id)
            }
        )

    return jsonify(
        {
            "status": "success",
            "data": restaurant.json()
        }
    )

@app.route("/restaurant/registration", methods=['POST'])
def add_new_restaurant():
    data = request.get_json()

    name = data['name']
    is_open = data['is_open']
    address = data['address']

    print(name,is_open,address)

    db.create_all()
    restaurant = Restaurant(name,is_open,address)

    try:
        db.session.add(restaurant)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured creating restaurant"
            }
        ), 500

    return jsonify(
        {
            "status": "success",
            "data": restaurant.json()
        }
    ), 201

@app.route("/restaurant/updaterestaurant/<rest_id>", methods=['PUT'])
def update_restaurant(rest_id):
    restaurant = Restaurant.query.filter_by(rest_id=rest_id).first()
   
    if restaurant is None:
        return jsonify(
            {
                "status": "error",
                "message": "restaurant of id {0} does not exists".format(rest_id)
            }
        )

    data = request.get_json()
    if 'name' in data:
        restaurant.name = data["name"]
    if 'is_open' in data:
        restaurant.is_open = data["is_open"]
    if 'address' in data:
        restaurant.address = data["address"]
    
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating restaurant"
            }
        ), 500
    return jsonify(
        {
            "status": "success",
            "data": restaurant.json()
        }
    )

###################################
#############  ITEMS  #############
###################################
class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    
    def __init__(self, name, price, description,category,img_url):

        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.img_url = img_url

    def json(self):
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "img_url": self.img_url
        }

@app.route("/restaurant/item")
def get_all_item():
    itemlist = Item.query.all()
    if len(itemlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "item": [item.json() for item in itemlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items."
        }
    ), 404

@app.route("/restaurant/item/<item_id>", methods=['GET'])
def get_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    # orderStatus = OrderStatus.query.filter_by(order_id=order_id).first()

    if item is None:
        return jsonify(
            {
                "status": "error",
                "message": "Item of id {0} does not exists".format(item_id)
            }
        )

    return jsonify(
        {
            "status": "success",
            "data": item.json()
        }
    )

@app.route("/restaurant/itemregistration", methods=['POST'])
def add_new_item():
    data = request.get_json()

    name = data['name']
    price = data['price']
    description = data['description']
    category = data['category']
    img_url = data['img_url']

    print(name,price,description,category,img_url)

    db.create_all()
    item = Item(name,price,description,category,img_url)

    try:
        db.session.add(item)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured creating item"
            }
        ), 500

    return jsonify(
        {
            "status": "success",
            "data": item.json()
        }
    ), 201

@app.route("/restaurant/itemupdate/<item_id>", methods=['PUT'])
def update_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
   
    if item is None:
        return jsonify(
            {
                "status": "error",
                "message": "item of id {0} does not exists".format(item_id)
            }
        )

    data = request.get_json()
    if 'name' in data:
        item.name = data["name"]
    if 'price' in data:
        item.price = data["price"]
    if 'description' in data:
        item.description = data["description"]
    if 'category' in data:
        item.category = data["category"]
    if 'img_url' in data:
        item.img_url = data["img_url"]
    
    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating item"
            }
        ), 500
    return jsonify(
        {
            "status": "success",
            "data": item.json()
        }
    )

###################################
########  RestaurantItems  ########
###################################

class RestaurantItems(db.Model):
    __tablename__ = 'restaurant_items'

    rest_id = db.Column(db.Integer, db.ForeignKey('restaurant.rest_id'), primary_key=True,autoincrement=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True,autoincrement=False)
    restaurant = db.relationship('Restaurant', primaryjoin='RestaurantItems.rest_id == Restaurant.rest_id', backref='restaurant_items')
    item = db.relationship('Item', primaryjoin='RestaurantItems.item_id == Item.item_id', backref='restaurant_items')
   
    def __init__(self,rest_id,item_id):
        
        self.rest_id = rest_id
        self.item_id = item_id

    def json(self):
        return {
            "rest_id": self.rest_id,
            "item_id": self.item_id
        }

# @app.route("/restaurant/restaurantitem/registration", methods=['POST'])

# def link_restaurant_item():
#     data = request.get_json()

#     rest_id = data['rest_id']
#     item_id = data['item_id']

#     print(rest_id,item_id)

#     db.create_all()
#     restaurantitem = Item(rest_id,item_id)

#     try:
#         db.session.add(restaurantitem)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "status": "error",
#                 "message": "An error occured linking restaurant and item"
#             }
#         ), 500

#     return jsonify(
#         {
#             "status": "success",
#             "data": restaurantitem.json()
#         }
#     ), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)