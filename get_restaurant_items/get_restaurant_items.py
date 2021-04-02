from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/get_restaurant_items/<rest_id>", methods=['GET'])
def get_restaurant_items(rest_id):
    print("entered")
    
    response = requests.get("http://restaurant-service:5000/restaurant/" + rest_id)
    
    if response.status_code != 200:
        return jsonify(
            {
                "status": "error",
                "message": "error in checking restaurant"
            }
        ), 500

    item_ids = response.json()["data"]["items"]
    items = []
    items_dict = {}

    for item_id_obj in item_ids:
        item_data = requests.get("http://restaurant-service:5000/restaurant/item/" + str(item_id_obj["item_id"]))
        print(item_data)
        # items.append(item_data.json()["data"])
        current_id = str(item_id_obj["item_id"])
        items_dict[current_id] = item_data.json()["data"]
            
    return jsonify(
        {
            "status": "success",
            "data": items_dict
        }
    )

    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)