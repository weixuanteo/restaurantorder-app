from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/get_orders/<rest_id>", methods=["GET"])
def get_restaurant_orders(rest_id):

    response = requests.get("http://order-service:5000/order/restaurant/" + rest_id)
    if response.status_code != 200:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling order service"
            }
        ), 500

    order_response = response.json()["data"]

    transformed_response = []
    for order_obj in order_response:
        order_items = []
        for order_item in order_obj["order_item"]:
            item_response = requests.get("http://restaurant-service:5000/restaurant/item/" + str(order_item["item_id"]))
            order_item["name"] = item_response.json()["data"]["name"]
            order_item["price"] = item_response.json()["data"]["price"] * order_item["qty"]
            order_items.append(order_item)
        order_obj["order_item"] = order_items
        transformed_response.append(order_obj)
    
    print(transformed_response)

    return jsonify(
        {
            "status": "success",
            "data": transformed_response
        }
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)