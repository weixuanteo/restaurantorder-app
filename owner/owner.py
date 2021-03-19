from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = SQLAlchemy(app)
query = """
    CREATE DATABASE
    IF NOT EXISTS {db}
""".format(db="owner")

engine = db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306',{})
engine.execute(query)
db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306/owner',{})

class Owner(db.Model):
    __tablename__ = 'owner'

    oid = db.Column(db.String(64), primary_key=True, autoincrement=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    
    def __init__(self, oid, name, email):
        self.oid = oid
        self.name = name
        self.email = email

    def json(self):
        return {
            "oid": self.oid,
            "name": self.name,
            "email": self.email
        }

@app.route("/owner/<oid>", methods=['GET'])
def get_owner(oid):
    owner = Owner.query.filter_by(oid=oid).first()
   
    if owner is None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of id {0} does not exists".format(oid)
            }
        )

    return jsonify(
        {
            "status": "success",
            "data": owner.json()
        }
    )

@app.route("/owner/registration", methods=['POST'])
def add_new_owner():
    data = request.get_json()

    owner_name = data["name"]
    owner_email = data["email"]
    owner_password = data["password"]

    print(owner_name, owner_email, owner_password)

    try:
        user = auth.create_user(
            email=owner_email,
            password=owner_password,
            display_name=owner_name
        )
    except firebase_admin._auth_utils.EmailAlreadyExistsError as e:
        print(e)
        return jsonify(
            {
                "status": "error",
                "message": "Email address already exists in Firebase Auth"
            }
        ), 500

    except ValueError as e:
        print(e)
        return jsonify(
            {
                "status": "error",
                "message": "Error occured creating user with Firebase Auth, check user properties"
            }
        ), 500
    
    # app.logger.info(user.uid, user.display_name, user.email)
    db.create_all()
    owner = Owner(user.uid, user.display_name, user.email)
    # app.logger.info(owner)

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
    owner = Owner.query.filter_by(oid=oid).first()
   
    if owner is None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of id {0} does not exists".format(oid)
            }
        )

    data = request.get_json()
    if "name" in data:
        owner.name = data["name"]
    if "email" in data:
        owner.email = data["email"]

    try:
        user = auth.update_user(
            oid,
            email=owner.email,
            display_name=owner.name
        )
    except exceptions.FirebaseError as e:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating on Firebase"
            }
        ), 500

    
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)