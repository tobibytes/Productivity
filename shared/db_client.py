from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is not None:
        return _db
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI is not set")
    _client = MongoClient(uri)
    _db = _client.db
    return _db

