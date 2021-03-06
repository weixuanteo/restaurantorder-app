from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

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
    items = db.relationship('RestaurantItems', backref='restaurant', lazy=True)
    
    def __init__(self, name, is_open, address):
        self.name = name
        self.is_open = is_open
        self.address = address

    def json(self):
        return {
            "rest_id": self.rest_id,
            "name": self.name,
            "is_open": self.is_open,
            "address": self.address,
            "items":[item.json() for item in self.items]
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
        ), 404

    return jsonify(
        {
            "status": "success",
            "data": restaurant.json()
        }
    )

@app.route("/restaurant", methods=['POST'])
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

@app.route("/restaurant/<rest_id>", methods=['PUT'])
def update_restaurant(rest_id):
    restaurant = Restaurant.query.filter_by(rest_id=rest_id).first()
   
    if restaurant is None:
        return jsonify(
            {
                "status": "error",
                "message": "restaurant of id {0} does not exists".format(rest_id)
            }
        ), 404

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
                "message": "An error occurred updating restaurant"
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
    img_url = db.Column(db.String(200))
    
    def __init__(self, name, price, description,category,img_url):

        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.img_url = img_url

    def json(self):
        return {
            "item_id": self.item_id,
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
        ), 404

    return jsonify(
        {
            "status": "success",
            "data": item.json()
        }
    )

@app.route("/restaurant/item/<item_id>", methods=['PUT'])
def update_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
   
    if item is None:
        return jsonify(
            {
                "status": "error",
                "message": "item of id {0} does not exists".format(item_id)
            }
        ), 404

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
                "message": "An error occurred updating item"
            }
        ), 500
    return jsonify(
        {
            "status": "success",
            "data": item.json()
        }
    )
  
@app.route("/restaurant/item/<item_id>", methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    print("hello")
    if item is None:
        return jsonify(
            {
                "status": "error",
                "message": "Item of id {0} does not exists".format(item_id)
            }
        )

    deleteItem = Item.query.get(item_id)
    print(deleteItem)
        
    try:
        db.session.delete(deleteItem)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured deleting the item"
            }
        ), 500

    return jsonify(
        {
            "status": "success",
            "message": "Successfully deleted"
        }
    )
###################################
########  RestaurantItems  ########
###################################

class RestaurantItems(db.Model):
    __tablename__ = 'restaurant_items'

    rest_id = db.Column(db.Integer, db.ForeignKey('restaurant.rest_id'), primary_key=True,autoincrement=False)
    item_id = db.Column(db.Integer, primary_key=True,autoincrement=False)
    # restaurant = db.relationship('Restaurant', primaryjoin='RestaurantItems.rest_id == Restaurant.rest_id', backref='restaurant_items')
    # item = db.relationship('Item', primaryjoin='RestaurantItems.item_id == Item.item_id', backref='restaurant_items')
   
    def __init__(self,rest_id,item_id):
        self.rest_id = rest_id
        self.item_id = item_id

    def json(self):
        return {
            # "rest_id": self.rest_id,
            "item_id": self.item_id
        }


@app.route("/restaurant/<rest_id>/item", methods=['POST'])
def add_item_by_restaurant(rest_id):
    data = request.get_json()
    
    name = data['name']
    price = data['price']
    description = data['description']
    category = data['category']
    img_url = data['img_url']

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
    
    
    rest_item = RestaurantItems(rest_id,item.item_id)
    restaurant = Restaurant.query.filter_by(rest_id=rest_id).first()
    if restaurant is None:
        return jsonify(
            {   
                "status":"error",
                "message": "Restaurant does not exists"
            }
        ), 404

    restaurant.items.append(rest_item)

    try:
        db.session.add(restaurant)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured linking restaurant and item"
            }
        ), 500

    return jsonify(
        {
            "status": "success",
            "data": restaurant.json()
        }
    ), 201


@app.route("/restaurant/<rest_id>/items", methods=["GET"])
def get_items_by_restaurant(rest_id):
    restaurant = Restaurant.query.filter_by(rest_id=rest_id).first()

    if restaurant is None:
        return jsonify(
            {
                "status": "error",
                "message": "Restaurant of id {0} does not exists".format(rest_id)
            }
        ), 404

    item_ids = restaurant.items;
    items = {}
    for id_obj in item_ids:
        item_id = id_obj.item_id
        item = Item.query.filter_by(item_id=item_id).first()
   
        if item is None:
            return jsonify(
                {
                    "status": "error",
                    "message": "item of id {0} does not exists".format(item_id)
                }
            ), 404
        
        items[item_id] = item.json()
    
    return jsonify(
        {
            "status": "success",
            "data": items
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)