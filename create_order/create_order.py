from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from os import environ
import logging
import amqp_setup
import pika

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

#create new order
@app.route("/create_order", methods=['POST'])
def create_new_order():
    data = request.get_json()

    # rest_id = data["rest_id"]
    # order_type = data["order_type"]
    # comments = data['comments']
    # order_items = data['order_items']
    # table_no = data['table_no']
    

    # print("checking post json", rest_id, order_type, comments,order_items,table_no)
    # new_order_data = {"rest_id": rest_id, "order_type": order_type, "comments": comments,'order_items':order_items,'table_no':table_no}
    # print(json.dumps(new_order_data))
    response = requests.post("http://order-service:5000/order/neworder", json=data)
    if response.status_code != 201:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling order service"
            }
        )

    order_id = response.json()["data"]["order_id"]
    order_status = response.json()["data"]["order_status"]["status"]

    queue_name = "order" + str(order_id)
    routing_key = str(order_id) + ".order.status"
    message_data = json.dumps({"order_id": order_id, "status": order_status})

    try:
        amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
        amqp_setup.channel.queue_bind(exchange=amqp_setup.exchangename, queue=queue_name, routing_key=routing_key)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=routing_key, body=message_data, properties=pika.BasicProperties(delivery_mode=2))
        print("\nOrder notification published to the RabbitMQ Exchange:", message_data)

    except Exception as e:
        print(e)
        return jsonify(
            {
                "status": "error",
                "message": "error in publishing message to rabbitmq"
            }
        )

    

    return jsonify(
        {
            "status": "success",
            "message": "order successfully added"
        }
    )



#create new order
@app.route("/update_order/<order_id>", methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    response = requests.post("http://order-service:5000/order/updateorder/" + order_id, json=data)

    if response.status_code != 201:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling restaurant service"
            }
        )
    
    return jsonify(
        {
            "status": "success",
            "message": "order successfully updated"
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)