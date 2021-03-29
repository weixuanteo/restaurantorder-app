from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
import logging

ON_RECEIVE_STATUS = 'Received'

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/rest_order'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# query = """
#     CREATE SCHEMA
#     IF NOT EXISTS `{db}`
# """.format(db="order")

# engine = db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306',{})
# engine.execute(query)
# db.create_engine('mysql+mysqlconnector://root:root@mariadb:3306/order',{})

#Order
class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    order_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    rest_id = db.Column(db.Integer, nullable=False)
    order_type = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.String(10), nullable=False)
    
    def __init__(self,rest_id,order_type,comments):
        
        self.rest_id = rest_id
        self.order_type = order_type
        self.comments = comments

    def json(self):
        order =  {
            
            "rest_id": self.rest_id,
            "order_type": self.order_type,
            "comments": self.comments
            # "order_status":self.order_status
            
        }

        order['order_item'] = []
        for item in self.order_item:
            order['order_item'].append(item.json())

        order['order_status'] = []
        for status in self.order_status:
            order['order_status'].append(status.json())

        # order["order_status"] = self.order_status

        return order


# what is the point of this table?
#Order Status
class OrderStatus(db.Model):
    __tablename__ = 'order_status'

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True,autoincrement=False)
    status = db.Column(db.String(10), nullable=False,primary_key=True, autoincrement=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    order = db.relationship(
        'Order', primaryjoin='OrderStatus.order_id == Order.order_id', backref='order_status')
   
    def __init__(self,status):
        self.status = status

    def json(self):
        return {"status": self.status}
            
#Order Item
## remember to add in item as foreign key
class OrderItem(db.Model):
    __tablename__ = 'order_item'

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True,autoincrement=False)
    item_id = db.Column(db.String(10), primary_key=True,autoincrement=False)
    qty = db.Column(db.Integer, nullable=False)
    order = db.relationship(
        'Order', primaryjoin='OrderItem.order_id == Order.order_id', backref='order_item')
        
   
    def __init__(self,item_id,qty):
        
        # self.order_id = order_id
        self.item_id = item_id
        self.qty = qty

    def json(self):
        return {
            "order_id": self.order_id,
            "item_id": self.item_id,
            "qty":self.qty
        }

@app.route("/order/<order_id>", methods=['GET'])
def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()

    if order is None:
        return jsonify(
            {
                "status": "error",
                "message": "Order of id {0} does not exists".format(order_id)
            }
        )

    return jsonify(
        {
            "status": "success",
            "data": order.json()
        }
    )

@app.route("/order/neworder", methods=['POST'])
def create_order():

    data = request.get_json()

    rest_id = data["rest_id"]
    order_type = data["order_type"]
    comments = data['comments']
    order_items = data['order_items']

    #print(rest_id,order_type,comments)

    db.create_all()
    order = Order(rest_id,order_type,comments)

    for item in order_items:
        order.order_item.append(OrderItem(item_id=item['item_id'],qty=item['qty']))
    
    status = OrderStatus(ON_RECEIVE_STATUS)
    order.order_status.append(status)

    try:

        db.session.add(order)
        db.session.commit()

    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured creating order"
            }
        ), 500
    
    return jsonify(
        {
            "status": "success",
            "data": order.json()
        }
    ), 201

@app.route("/order/updateorder/<order_id>", methods=['PUT'])
def update_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    
    if order is None:
        return jsonify(
            {
                "status": "error",
                "message": "order of id {0} does not exists".format(order_id)
            }
        )

    data = request.get_json()
    if 'rest_id' in data:
        order.rest_id = data["rest_id"]
    if 'order_type' in data:
        order.email = data["order_type"]
    if 'comments' in data:
        order.comments = data["comments"]
    if 'order_items' in data:

        order_status = OrderItem.query.filter_by(order_id=order_id).delete()

        try:
        #db.session.add(order)
            db.session.commit()
        except:
            return jsonify(
                {
                    "status": "error",
                    "message": "An error occured deleting order_item"
                }
            ), 500


        for item in data['order_items']:
            order.order_item.append(OrderItem(item_id=item['item_id'],qty=item['qty']))
    
    try:
        #db.session.add(order)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating order"
            }
        ), 500


    return jsonify(
        {
            "status": "success",
            "data": order.json()
        }
    )


@app.route("/order/updatestatus/<order_id>", methods=['PUT'])
def update_status(order_id):
    orderStatus = OrderStatus.query.filter_by(order_id=order_id).first()
   
    if orderStatus is None:
        return jsonify(
            {
                "status": "error",
                "message": "orderStatus of id {0} does not exists".format(order_id)
            }
        )

    data = request.get_json()
    if data['status']:
        orderStatus.status = data["status"]
    
    try:
        # db.session.add(order)
        db.session.commit()
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured updating order"
            }
        ), 500


    return jsonify(
        {
            "status": "success",
            "data": orderStatus.json()
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
