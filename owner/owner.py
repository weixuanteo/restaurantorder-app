from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

db = SQLAlchemy(app)
# query = """
#     CREATE SCHEMA
#     IF NOT EXISTS `{db}`
# """.format(db="owner")

# engine = db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306',{})
# engine.execute(query)
# db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306/owner',{})

class Owner(db.Model):
    __tablename__ = 'owner'

    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {
            "oid": self.oid,
            "name": self.name,
            "email": self.email,
            "password": self.password
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

    owner = Owner.query.filter_by(email=owner_email).first()
    if owner is not None:
        return jsonify(
            {
                "status": "error",
                "message": "Owner of email {0} already exists".format(owner.email)
            }
        )
    
    # app.logger.info(user.uid, user.display_name, user.email)
    hash_salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(owner_password.encode('utf8'), hash_salt)

    db.create_all()
    owner = Owner(owner_name, owner_email, hash_password)
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
        )
    
    is_authenticated = bcrypt.checkpw(owner_password.encode('utf8'), owner.password.encode('utf8'))
    if (not is_authenticated):
        return jsonify(
            {
                "status": "error",
                "message": "Auth failed"
            }
        )
    
    return jsonify(
            {
                "status": "success",
                "data": owner.json() 
            }
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)