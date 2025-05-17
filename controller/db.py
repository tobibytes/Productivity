
from pymongo.mongo_client import MongoClient
import os
import bson
from dotenv import load_dotenv
load_dotenv()
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
            self.modules_col = self.db.create_collection('modules')
            self.module_items_col = self.db.create_collection('module_items')
            self.assignments_col = self.db.create_collection('assignments')
            self.submissions_col = self.db.create_collection('submissions')
            self.pricing_col = self.db.create_collection('pricing')
            self.flashcards_col = self.db.create_collection('flashcards')
            self.notes_col = self.db.create_collection('notes')

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
            # self.modules_col.create_index('module_id', unique=True)
            # self.module_items_col.create_index('module_item_id', unique=True)
            # self.assignments_col.create_index('assignment_id', unique=True)
            # self.submissions_col.create_index('submission_id', unique=True)
            self.user_col.create_index('status')
            self.modules_col.create_index('course_id')
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
        
    def get_user_courses_modules_module_items_id(self, email):
        user_info = self.get_user(email)
        courses = user_info['courses']
        result = []
        for course in courses:
            course_modules = db.get_modules(course['course_id'])
            for module in course_modules:
                course_module_items = db.get_module_items(module['module_id'])
                for module_item in course_module_items:
                    data = {
                        "course_id": course["course_id"],
                        "module_id": module["module_id"],
                        "module_item_id": module_item["module_item_id"],
                        "email": user_info["email"]
                    }
                    result.append(data)
        return result
        
    def get_modules(self, course_id):
        """
        Get all modules for a course from the database.
        """
        modules = self.modules_col.find({'module_course_id': course_id})
        if modules:
            return [self.format_for_db(module) for module in modules]
        else:
            return None
        
    def get_module(self, course_id, module_id):
        """
        Get a module from the database.
        """
        module = self.modules_col.find_one({'module_id': module_id, 'module_course_id': course_id})
        if module:
            return self.format_for_db(module)
        else:
            return None
        
    def add_module_item(self, module_item):
        """
        Add a module item to the database.
        """
        self.module_items_col.insert_one(module_item)
    
    def get_module_items(self, module_item_module_id):
        """
        Get all module items for a module from the database.
        """
        module_items = self.module_items_col.find({'module_item_module_id': module_item_module_id})
        if module_items:
            return [self.format_for_db(module_item) for module_item in module_items]
        else:
            return None
        
    def get_module_item(self, module_item_module_id, module_item_id):
        """
        Get a module item from the database.
        """
        module_item = self.module_items_col.find_one({'module_item_id': module_item_id, 'module_item_module_id': module_item_module_id})
        if module_item:
            return self.format_for_db(module_item)
        else:
            return None
    
    def add_assignment(self, assignment):
        """
        Add an assignment to the database.
        """
        self.assignments_col.insert_one(assignment)
        
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