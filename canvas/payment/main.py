

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


  
@app.route("/pricings")
def get_pricings():
    """
    Get all pricings
    """
    
    pricings = db.get_pricings()
    email = request.args.get('email', None)
    if email or email != "null":
        pricing_id = db.get_user_pricing(email=email)
        for idx, pricing in enumerate(pricings):
            if pricings[idx]['id'] == pricing_id:
                pricings[idx]['is_active'] = True
            else:
                pricings[idx]['is_active'] = False
    return {"pricings": pricings}

class POSTSUBSCRIBETOPRICING(BaseModel):
  email: str
  pricing_id: str
  
@app.route("/users/pricings/", methods=["POST"])
def suscribe_to_pricing():
  data = request.get_json()
  data = POSTSUBSCRIBETOPRICING(**data)
  if not data:
      return {"error": "Could not verify user"}
    email = data.email
    pricing_id = data.pricing_id
    user = db.get_user(email=email)
    if not user:
        return {"error": "Could not verify user"}
    result = db.subsribe_user(email=email, pricing_id=pricing_id)
    return {"status": "User subscribed to pricing successfully", "success": True}
  

if __name__ == "__main__":
  app.run(port=4242, debug=True, host='0.0.0.0')