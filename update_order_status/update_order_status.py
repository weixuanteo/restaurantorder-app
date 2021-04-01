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

#update order status
@app.route("/update_order_status/<order_id>", methods=['PUT'])
def update_order_status(order_id):
    print(order_id)
    data = request.get_json()
    response = requests.put("http://order-service:5000/order/updatestatus/" + order_id, json=data)

    if response.status_code != 200:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling order service"
            }
        )
    
    order_status = response.json()["data"]["status"]

    queue_name = "order" + str(order_id)
    routing_key = str(order_id) + ".order.status"
    message_data = json.dumps({"order_id": order_id, "status": order_status})

    try:
        amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
        amqp_setup.channel.queue_bind(exchange=amqp_setup.exchangename, queue=queue_name, routing_key=routing_key)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=routing_key, body=message_data, properties=pika.BasicProperties(delivery_mode=2))
        print("\nUpdated Order notification published to the RabbitMQ Exchange:", message_data)

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
            "message": "Order status successfully updated"
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)