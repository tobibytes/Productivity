
from pymongo.mongo_client import MongoClient
import os
uri = os.getenv("mongo_uri")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
summary_db = client.summary

try:
    summary_col = summary_db.create_collection('summary')
except:
    summary_col = summary_db.summary

def add_summary_to_db(summary):
    print('summary')
    summary['status'] = 0
    summary_col.insert_one(summary)