
from pymongo.mongo_client import MongoClient
import os
import bson
uri = os.getenv("mongo_uri")

client = MongoClient(uri)

summary_db = client.summary
try:
    summary_col = summary_db.create_collection('summary')
except:
    summary_col = summary_db.summary

def add_summary_to_db(summary):
    summary['status'] = 0
    summary_col.insert_one(summary)

def get_summary_from_db():
    summaries = summary_col.find().to_list()
    summaries = [format_for_db(summary) for summary in summaries]
    return summaries

def get_summary_from_db_test():
    summaries = summary_col.find().to_list()
    summaries = [summary for summary in summaries]
    return summaries

def update_summary_status_db(id, status):
    summary_col.update_one({'_id': bson.ObjectId(id)}, {'status': status})

def format_for_db(summary):
    summary = remove_bson(summary)
    return summary

def remove_bson(summary : dict):
    summary['_id'] = str(summary['_id'])
    return summary