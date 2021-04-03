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
        )

    return jsonify(
        {
            "status": "success",
            "message": "Account ID of {0} successfully deleted".format(id)
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)