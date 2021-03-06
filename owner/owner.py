from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import bcrypt
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


class Owner(db.Model):
    __tablename__ = 'owner'

    owner_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    restaurants = db.relationship('OwnerRestaurant', backref='owner', lazy=True)
    stripe_account = db.Column(db.String(128), nullable=True)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "restaurants": [restaurant.json() for restaurant in self.restaurants],
            "stripe_account": self.stripe_account
        }

class OwnerRestaurant(db.Model):
    __tablename__ = 'owner_restaurant'

    rest_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'), nullable=False)

    def __init__(self, rest_id, owner_id):
        self.rest_id = rest_id
        self.owner_id = owner_id

    def json(self):
        return {
            "rest_id": self.rest_id
        }


@app.route("/owner/<oid>", methods=['GET'])
def get_owner(oid):
    owner = Owner.query.filter_by(owner_id=oid).first()
   
    if owner is None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of id {0} does not exists".format(oid)
            }
        ), 404

    return jsonify(
        {
            "status": "success",
            "data": owner.json()
        }
    ), 200

@app.route("/owner/registration", methods=['POST'])
def add_new_owner():
    data = request.get_json()

    owner_name = data["name"]
    owner_email = data["email"]
    owner_password = data["password"]

    db.create_all()

    owner = Owner.query.filter_by(email=owner_email).first()
    if owner is not None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of email {0} already exists".format(owner.email)
            }
        ), 409
    
    hash_salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(owner_password.encode('utf8'), hash_salt)

    owner = Owner(owner_name, owner_email, hash_password)

    try:
        db.session.add(owner)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured creating owner"
            }
        ), 500
    
    return jsonify(
        {
            "status": "success",
            "data": owner.json()
        }
    ), 201

@app.route("/owner/<oid>", methods=['PUT'])
def update_owner(oid):
    owner = Owner.query.filter_by(owner_id=oid).first()
   
    if owner is None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of id {0} does not exists".format(oid)
            }
        ), 404

    data = request.get_json()
    if "name" in data:
        owner.name = data["name"]
    if "email" in data:
        owner.email = data["email"]
    if "stripe" in data:
        owner.stripe_account = data["stripe"]

    try:
        db.session.add(owner)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating owner"
            }
        ), 500


    return jsonify(
        {
            "status": "success",
            "data": owner.json()
        }
    )

@app.route("/owner/auth", methods=['POST'])
def auth_owner():

    data = request.get_json()
    
    owner_email = data["email"]
    owner_password = data["password"]

    owner = Owner.query.filter_by(email=owner_email).first()
    if owner is None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner does not exists"
            }
        ), 401
    
    is_authenticated = bcrypt.checkpw(owner_password.encode('utf8'), owner.password.encode('utf8'))
    if (not is_authenticated):
        return jsonify(
            {
                "status": "error",
                "message": "Auth failed"
            }
        ), 401
    
    return jsonify(
            {
                "status": "success",
                "data": owner.json() 
            }
        ), 200

@app.route("/owner/restaurant", methods=['POST'])
def add_restaurant_by_owner():
    data = request.get_json()

    owner_id = data["owner_id"]
    rest_id = data["rest_id"]

    owner_rest = OwnerRestaurant(rest_id, owner_id)
    owner = Owner.query.filter_by(owner_id=owner_id).first()
    if owner is None:
            return jsonify(
            {
                "status": "error",
                "message": "Owner does not exists" 
            }
        ), 404
        
    owner.restaurants.append(owner_rest)
    try:
        db.session.add(owner)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured adding restaurant to owner"
            }
        ), 500
    
    return jsonify(
            {
                "status": "success",
                "data": owner.json() 
            }
        ), 200

@app.route("/owner/account/<rest_id>", methods=["GET"])
def get_stripe_account_by_restaurant(rest_id):
    ownerRestaurant = OwnerRestaurant.query.filter_by(rest_id=rest_id).first()
    owner = Owner.query.filter_by(owner_id=ownerRestaurant.owner_id).first()

    return jsonify({
        "status": "success",
        "data": owner.json()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)