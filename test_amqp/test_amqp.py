from flask import Flask, request, jsonify
import json
import logging
import amqp_setup
import traceback
import pika

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/test", methods=['POST'])
def test_amqp():
    data = request.get_json()

    order_id = str(data["order_id"])
    status = data["status"]

    queue_name = "order" + order_id
    routing_key = order_id + ".order.status"
    try:
        amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
        amqp_setup.channel.queue_bind(exchange=amqp_setup.exchangename, queue=queue_name, routing_key=routing_key)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key=routing_key, body=json.dumps(data), properties=pika.BasicProperties(delivery_mode=2))
        print("\nOrder notification published to the RabbitMQ Exchange:", data)

    except Exception as e:
        print(e)
    
    return jsonify(
        {
            "message": "Success!"
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)