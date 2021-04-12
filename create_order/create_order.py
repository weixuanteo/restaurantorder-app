from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from os import environ
import logging
import sys

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/create_order", methods=['POST'])
def create_new_order():
    data = request.get_json()

    response = requests.post("http://order-service:5000/order", json=data)
    if response.status_code != 201:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling order service"
            }
        ), 500

    ownerResponse = requests.get("http://owner-service:5000/owner/account/" + str(data["rest_id"]))

    account_id = ownerResponse.json()["data"]["stripe_account"]

    paymentData = {
        "account_id": account_id,
        "order" : {
            "price": data["price"]
        }
    }

    paymentResponse = requests.post("http://payment-service:5000/payment", json=paymentData)

    return jsonify(
        {
            "status": "success",
            "data": {
                "session_id": paymentResponse.json()["data"]["id"],
                "order": response.json()["data"]
            }
        }
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)