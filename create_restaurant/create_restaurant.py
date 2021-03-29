from flask import Flask, request, jsonify
import requests
import json
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/new_restaurant/<oid>", methods=['POST'])
def create_new_restaurant(oid):
    data = request.get_json()
    rest_name = data["name"]
    is_open = data["is_open"]
    rest_address = data["address"]

    response = requests.get("http://owner-service:5000/owner/" + oid)
    
    if response.status_code != 200:
        return jsonify(
            {
                "status": "error",
                "message": "error in checking owner"
            }
        )
    
    response_data = response.json()

    owner_id = response_data["data"]["owner_id"]

    print("checking post json", rest_name, is_open, rest_address)
    new_restaurant_data = {"name": rest_name, "is_open": is_open, "address": rest_address}
    print(json.dumps(new_restaurant_data))
    response = requests.post("http://restaurant-service:5000/restaurant", json=new_restaurant_data)

    if response.status_code != 201:
        return jsonify(
            {
                "status": "error",
                "message": "error in calling restaurant service"
            }
        )
    
    rest_id = response.json()["data"]["rest_id"]
    body = {"owner_id": owner_id, "rest_id": rest_id}

    response = requests.post("http://owner-service:5000/owner/restaurant", json=body)
    
    if response.status_code != 200:
                return jsonify(
            {
                "status": "error",
                "message": "error in calling owner service"
            }
        )
    
    return jsonify(
        {
            "status": "success",
            "message": "Restaurant successfully added"
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)