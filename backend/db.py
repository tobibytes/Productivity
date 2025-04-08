
from pymongo.mongo_client import MongoClient
import os
uri = os.getenv("mongo_uri")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
summary_db = client.summary
summary_col = summary_db.summary

def add_summary_to_db(summary):
    summary_col.insert_one(summary)

def get_summary_from_db():
    summaries = summary_col.find().to_list()
    summaries = [format_for_db(summary) for summary in summaries]
    return summaries

def format_for_db(summary):
    summary = remove_bson(summary)
    summary['status'] = 0
    return summary

def remove_bson(summary : dict):
    summary['_id']= ''
    return summary