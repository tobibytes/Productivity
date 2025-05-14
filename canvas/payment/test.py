import stripe
stripe.api_key = "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"

# print(stripe.Price.list(limit=3))

# products = stripe.Product.list(limit=3)
# print(products)

print(stripe.Price.list(limit=3))