
from pymongo.mongo_client import MongoClient
import os
import bson
uri = os.getenv("MONGODB_URI")
class Database:
    def __init__(self):
        """
        Initialize the database connection.
        """
        self.uri = uri
        self.client = MongoClient(uri)
        self.db = self.client.db
        try:
            self.user_col = self.db.create_collection('user')
            self.pricing_col = self.db.create_collection('pricing')

        except:
            self.user_col = self.db.user
            self.pricing_col = self.db.pricing
        try:
            self.user_col.create_index('email', unique=True)
            self.user_col.create_index('status')   
        except:
            pass
            
        
    def get_user(self, email):
        """
        Get a user from the database.
        """
        user = self.user_col.find_one({'email': email})
        if user:
            return self.format_for_db(user)
        else:
            return None
        
        
    def add_pricing(self, pricing):
        """
        Add a pricing to the database.
        """
        self.pricing_col.insert_one(pricing)
        
    def get_pricings(self):
        """
        Get a pricing from the database.
        """
        pricing = self.pricing_col.find({})
        if pricing:
            return [self.format_for_db(pricing) for pricing in pricing]
        else:
            return None
    def subscribe_user(self, email, pricing_id):
        """
        Subscribe a user to a pricing.
        """
        self.user_col.update_one({'email': email}, {'$set': {'pricing_id': pricing_id}})
        
        
    def get_user_pricing(self, email):
        """
        Get a user's pricing.
        """
        user = self.user_col.find_one({'email': email})
        if user:
            return user['pricing_id']
        
    def unsubscribe_user(self, email):
        """
        Unsubscribe a user from a pricing.
        """
        self.user_col.update_one({'email': email}, {'$set': {'pricing_id': None}})
        
    def format_for_db(self, data):
        """
        Format the data for the database.
        """
        data = self.remove_bson(data)
        return data
    
    def remove_bson(self, data):
        """
        Remove the BSON ObjectId from the data.
        """
        data['_id'] = str(data['_id'])
        return data