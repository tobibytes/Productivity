
from pymongo.mongo_client import MongoClient
import os
import bson
uri = os.getenv("MONGODB_URI")

prices = [
    {"active":True,"pricing_table_id":"prctbl_1RNm71LpjISvJMPEWIHks5Wn","billing_scheme":"per_unit","created":{"$numberInt":"1747017522"},"currency":"usd","custom_unit_amount":None,"id":"price_1RNmGMLpjISvJMPEvgNfdEDl","livemode":True,"lookup_key":None,"metadata":{},"nickname":None,"object":"price","product":"prod_SIN0ctCHe3D4oN","recurring":{"interval":"month","interval_count":{"$numberInt":"3"},"meter":None,"trial_period_days":None,"usage_type":"licensed"},"tax_behavior":"unspecified","tiers_mode":None,"transform_quantity":None,"type":"recurring","unit_amount":{"$numberInt":"15000"},"unit_amount_decimal":"15000"},
    {"active":True,"pricing_table_id":"prctbl_1RNmDdLpjISvJMPEikWlXfpm","billing_scheme":"per_unit","created":{"$numberInt":"1747017280"},"currency":"usd","custom_unit_amount":None,"id":"price_1RNmCSLpjISvJMPEypkBXE5y","livemode":True,"lookup_key":None,"metadata":{},"nickname":None,"object":"price","product":"prod_SIMuDiqE5GBkdm","recurring":{"interval":"month","interval_count":{"$numberInt":"3"},"meter":None,"trial_period_days":None,"usage_type":"licensed"},"tax_behavior":"unspecified","tiers_mode":None,"transform_quantity":None,"type":"recurring","unit_amount":{"$numberInt":"3000"},"unit_amount_decimal":"3000"},
    {"active":True,"pricing_table_id":"prctbl_1RNmHQLpjISvJMPEbVdjGk3J","billing_scheme":"per_unit","created":{"$numberInt":"1747016424"},"currency":"usd","custom_unit_amount":None,"id":"price_1RNlyeLpjISvJMPEewIklNAm","livemode":True,"lookup_key":None,"metadata":{},"nickname":None,"object":"price","product":"prod_SIMi1qr8MLzyyy","recurring":{"interval":"month","interval_count":{"$numberInt":"3"},"meter":None,"trial_period_days":None,"usage_type":"licensed"},"tax_behavior":"unspecified","tiers_mode":None,"transform_quantity":None,"type":"recurring","unit_amount":{"$numberInt":"0"},"unit_amount_decimal":"0"}
]

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
            self.modules_col = self.db.create_collection('modules')
            self.module_items_col = self.db.create_collection('module_items')
            self.assignments_col = self.db.create_collection('assignments')
            self.submissions_col = self.db.create_collection('submissions')
            self.notes_col = self.db.create_collection('notes')
            self.pricing_col = self.db.create_collection('pricing')
            self.flashcards_col = self.db.create_collection('flashcards')

        except:
            self.user_col = self.db.user
            self.modules_col = self.db.modules
            self.module_items_col = self.db.module_items
            self.assignments_col = self.db.assignments
            self.submissions_col = self.db.submissions
            self.pricing_col = self.db.pricing
            self.flashcards_col = self.db.flashcards
            self.notes_col = self.db.notes
        try:
            self.user_col.create_index('email', unique=True)
            self.user_col.create_index('status')   
        except:
            pass
        self.pricing_col.insert_many(prices)
        
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
        if '_id' in data:
            data['_id'] = str(data['_id'])
            return data
        data