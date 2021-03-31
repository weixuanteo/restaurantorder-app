from flask import Flask, request, jsonify
import requests
import json
from os import environ
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

#update order status
@app.route("/update_order_status/<order_id>", methods=['PUT'])
def update_order_status(order_id):
    print(order_id)
    data = request.get_json()
    response = requests.put("http://order-service:5000/order/updatestatus/" + order_id, json=data)
    # r = requests.put('http://order-service:5000/order/updatestatus/'+order_id, data ={'key':'value'})
    if response.status_code != 200:
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