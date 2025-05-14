# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import os
import stripe

from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()
from db import Database
db = Database()

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.getenv("STRIPE_API_KEY")
# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.getenv("STRIPE_ENDPOINT_SECRET", "")

app = Flask(__name__)
@app.route('/index')
def read_root():
    return {"Hello": "World"}
@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'charge.failed':
      charge = event['data']['object']
      data = charge
    # elif event['type'] == 'charge.pending':
    #   charge = event['data']['object']
    #   data = charge
    elif event['type'] == 'charge.succeeded':
      charge = event['data']['object']
      data = charge
    elif event['type'] == 'checkout.session.completed':
      session = event['data']['object']
      data = session
      db.subscribe_user(session['customer_email'], session['client_reference_id'])
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))
    return jsonify(success=True)
  
if __name__ == "__main__":
  app.run(port=4242, debug=True, host='0.0.0.0')