
from pymongo.mongo_client import MongoClient
import os
import bson
from dotenv import load_dotenv
load_dotenv()
#         """
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
            # self.modules_col.create_index('module_id', unique=True)
            # self.module_items_col.create_index('module_item_id', unique=True)
            # self.assignments_col.create_index('assignment_id', unique=True)
            # self.submissions_col.create_index('submission_id', unique=True)
            self.user_col.create_index('status')
            self.modules_col.create_index('course_id')
        except:
            pass
            
            
    def add_user(self, user):
        """
        Add a user to the database.
        """
        user['status'] = 0
        self.user_col.insert_one(user)
        
    def get_user(self, email):
        """
        Get a user from the database.
        """
        user = self.user_col.find_one({'email': email})
        if user:
            return self.format_for_db(user)
        else:
            return None
        
    def add_module(self, module):
        """
        Add a module to the database.
        """
        self.modules_col.insert_one(module)
        
    def get_note(self, module_item_id, email):
        return self.format_for_db(self.notes_col.find_one({'module_item_id': module_item_id, 'email': email}))
        
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
        
    def get_assignment(self, course_id, assignment_id):
        """
        Get an assignment from the database.
        """
        assignment = self.assignments_col.find_one({'assignment_id': assignment_id, 'assignment_course_id': course_id})
        if assignment:
            return self.format_for_db(assignment)
        else:
            return None
    def get_assignments(self, course_id):
        """
        Get all assignments for a course from the database.
        """
        assignments = self.assignments_col.find({'assignment_course_id': course_id})
        if assignments:
            return [self.format_for_db(assignment) for assignment in assignments]
        else:
            return None
    def add_submission(self, submission):
        """
        Add a submission to the database.
        """
        self.submissions_col.insert_one(submission)
    def get_submission(self, submission_id):
        """
        Get a submission from the database.
        """
        submission = self.submissions_col.find_one({'submission_id': submission_id})
        if submission:
            return self.format_for_db(submission)
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