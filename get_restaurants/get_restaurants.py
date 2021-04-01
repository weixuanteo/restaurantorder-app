from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

@app.route("/get_restaurants/<oid>", methods=['GET'])
def get_owner_restaurants(oid):
    
    response = requests.get("http://owner-service:5000/owner/" + oid)
    
    if response.status_code != 200:
        return jsonify(
            {
                "status": "error",
                "message": "error in checking owner"
            }
        ), 500

    rest_ids = response.json()["data"]["restaurants"]
    restaurants = []

    for rest_id_obj in rest_ids:
        rest_data = requests.get("http://restaurant-service:5000/restaurant/" + str(rest_id_obj["rest_id"]))
        restaurants.append(rest_data.json()["data"])

    return jsonify(
        {
            "status": "success",
            "data": restaurants
        }
    )

    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)