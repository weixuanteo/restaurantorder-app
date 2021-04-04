from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
import pika

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

hostname = "esd-rabbitmq"
port = 5672


order_status = None

@app.route("/notification/<order_id>", methods=["GET"])
def get_order_notifications(order_id):
    queue_name = "order" + order_id

    credentials = pika.PlainCredentials('serviceuser', 'serviceuser')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
        credentials=credentials # these parameters to prolong the expiration time (in seconds) of the connection
    ))

    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue=queue_name)
    if method_frame is None:
        connection.close()
        return jsonify({
            "status": "fail",
            "message": "No message available"
        })
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    message = body.decode('unicode_escape')
    message_json = json.loads(message)

    if message_json["status"] == 3:
        channel.queue_delete(queue_name)
    
    connection.close()
    
    return jsonify(
        {
            "status": "success",
            "data": message_json
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)