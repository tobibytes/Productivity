from abc import ABC

class AbstractDatabase(ABC):
    def __init__(self):
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
        user = self.user_col.find_one({'email': email})
        if user:
            return self.format_for_db(user)
        else:
            return None

    def add_user(self, user):
        user['status'] = 0
        self.user_col.insert_one(user)
        

    def get_modules(self, course_id):
        modules = self.modules_col.find({'module_course_id': course_id})
        if modules:
            return [self.format_for_db(module) for module in modules]
        else:
            return None

    def get_module(self, course_id, module_id):
        module = self.modules_col.find_one({'module_id': module_id, 'module_course_id': course_id})
        if module:
            return self.format_for_db(module)
        else:
            return None

    def add_module(self, module):
        self.modules_col.insert_one(module)

    def add_module_item(self, module_item):
        self.module_items_col.insert_one(module_item)

    def get_module_items(self, module_item_module_id):
        module_items = self.module_items_col.find({'module_item_module_id': module_item_module_id})
        if module_items:
            return [self.format_for_db(module_item) for module_item in module_items]
        else:
            return None

    def get_module_item(self, module_item_module_id, module_item_id):
        module_item = self.module_items_col.find_one({'module_item_id': module_item_id, 'module_item_module_id': module_item_module_id})
        if module_item:
            return self.format_for_db(module_item)
        else:
            return None

    def add_assignment(self, assignment):
        self.assignments_col.insert_one(assignment)

    def get_assignment(self, course_id, assignment_id):
        assignment = self.assignments_col.find_one({'assignment_id': assignment_id, 'assignment_course_id': course_id})
        if assignment:
            return self.format_for_db(assignment)
        else:
            return None

    def get_assignments(self, course_id):
        assignments = self.assignments_col.find({'assignment_course_id': course_id})
        if assignments:
            return [self.format_for_db(assignment) for assignment in assignments]
        else:
            return None

    def add_submission(self, submission):
        self.submissions_col.insert_one(submission)

    def get_submission(self, submission_id):
        submission = self.submissions_col.find_one({'submission_id': submission_id})
        if submission:
            return self.format_for_db(submission)
        else:
            return None
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



class NoteDatabase(AbstractDatabase):
    def __init__(self, db):
        self.db = db
        self.notes_col = db.notes
        self.user_col = db.users
        self.modules_col = db.modules
        self.module_items_col = db.module_items
        self.assignments_col = db.assignments
        self.submissions_col = db.submissions
        self.pricing_col = db.pricing

    def add_note(self, data):
        self.notes_col.insert_one(data)

    def get_note(self, module_item_id, email):
        return self.format_for_db(self.notes_col.find_one({'module_item_id': module_item_id, 'email': email}))
              
    def add_flashcard(self, data):
        self.flashcards_col.insert_one(data)
    
class PaymentDatabase(AbstractDatabase):
    def __init__(self, db):
        self.db = db
        self.user_col = db.users
        self.pricing_col = db.pricing
        self.subscriptions_col = db.subscriptions
    def subscribe_user(self, email, pricing_id):
        self.user_col.update_one({'email': email}, {'$set': {'pricing_id': pricing_id}})

    def unsubscribe_user(self, email):
        self.user_col.update_one({'email': email}, {'$set': {'pricing_id': None}})

    def get_user_pricing(self, email):
        user = self.user_col.find_one({'email': email})
        if user:
            return user['pricing_id']
        
    def add_pricing(self, pricing):
        self.pricing_col.insert_one(pricing)

    def get_pricings(self):
        pricing = self.pricing_col.find({})
        if pricing:
            return [self.format_for_db(p) for p in pricing]
        else:
            return None 