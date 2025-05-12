#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import os
from flask import Flask, redirect, jsonify, json, request, current_app
from flask_cors import CORS
import stripe

# This is your test secret API key.
stripe.api_key = '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'

app = Flask(__name__, static_url_path='', static_folder='public')
CORS(app)

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/', methods=['GET'])
def get_index():
    return current_app.send_static_file('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        lookup_key = data['lookup_key']
        print(stripe.Product.list(limit=3))
        prices = stripe.Price.list(
            # lookup_keys=[lookup_key],
            # expand=['data.product']
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': prices.data[0].id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/create-portal-session', methods=['POST'])
def customer_portal():
    try:
        data = request.get_json()
        checkout_session_id = data['session_id']

        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=YOUR_DOMAIN,
        )
        return jsonify({'url': portalSession.url})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = 'whsec_12345'
    request_data = json.loads(request.data)

    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data,
                sig_header=signature,
                secret=webhook_secret
            )
            data = event['data']
            event_type = event['type']
        except Exception as e:
            return str(e), 400
    else:
        data = request_data['data']
        event_type = request_data['type']

    data_object = data['object']

    print('🔔 Event:', event_type)

    if event_type == 'checkout.session.completed':
        print('✅ Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('📅 Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('📦 Subscription created:', event.id)
    elif event_type == 'customer.subscription.updated':
        print('🔄 Subscription updated:', event.id)
    elif event_type == 'customer.subscription.deleted':
        print('❌ Subscription canceled:', event.id)
    elif event_type == 'entitlements.active_entitlement_summary.updated':
        print('🎯 Entitlement summary updated:', event.id)

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=4242, host='0.0.0.0')