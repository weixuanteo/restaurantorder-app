from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from os import environ
import logging
import stripe

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

stripe.api_key = environ.get('STRIPE_API_KEY')

@app.route("/payment", methods=["POST"])
def new_payment():
    data = request.get_json()

    account_id = data["account_id"]
    order = data["order"]
    # order_items = data["order_items"]

    # line_items = []
    # for order_item in order_items:
    #     item = {}
    #     item["name"] = order_item["name"]
    #     item["amount"] = order_item["qty"]
    #     item["currency"] = "sgd"
    #     item["amount"] = order_item["price"]
    #     line_items.append(item)

    # print(line_items)
    # return

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'name': 'Lestoran Meal',
            'amount': int(order["price"] * 100),
            'currency': 'sgd',
            'quantity': 1
        }],
        payment_intent_data={
            'application_fee_amount': 1,
            'transfer_data': {
                'destination': account_id,
            },
        },
        success_url="http://localhost:5500/bootClientUI/orderStatus.html",
        cancel_url="http://localhost:5500/bootClientUI/home.html"
    )

    return jsonify({
        "status": "success",
        "data": {
            "id": session.id
        }
    })

@app.route("/payment/account/url", methods=["GET"])
def create_express_account():

    account = stripe.Account.create(
        type='express'
    )

    print(account)

    account_links = stripe.AccountLink.create(
        account=account.id,
        refresh_url='http://localhost:5500/AdminUI/login.html',
        return_url='http://localhost:5500/AdminUI/home.html',
        type='account_onboarding'
    )

    print(account_links)
    print(account_links.url)

    return jsonify(
        {
            "status": "success",
            "data": {
                "id": account.id,
                "url": account_links.url
            }

        }   
    ), 200


@app.route("/payment/account/<id>", methods=["DELETE"])
def delete_express_account(id):
    try:
        stripe.Account.delete(id)
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured attempting to delete the account"
            }
        ), 500

    return jsonify(
        {
            "status": "success",
            "message": "Account ID of {0} successfully deleted".format(id)
        }
    )

@app.route("/payment/dashboard/<id>", methods=["GET"])
def get_account_dashboard_link(id):
    login = None
    try:
        login = stripe.Account.create_login_link(
            id,
        )
    except:
        return jsonify(
            {
                "status": "error",
                "message": "An error occured attempting to create login link"
            }
        ), 500

    return jsonify({
        "status": "success",
        "data": login
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)