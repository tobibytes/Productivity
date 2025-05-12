# import app
# import time
# pubsub_publisher = app.PubSub('redis')
# redis = app.get_redis('redis')
# time.sleep(5)
# while True:
#     start_date = app.get_start_date(redis)
#     course_codes = app.process_context_codes_for_url(app.Config.COURSES_ID)
#     headers = app.Config.CANVAS_HEADERS
#     canvas_url = app.Config.CANVAS_API_URL
#     announcements= app.get_announcements_from_canvas(canvas_url=canvas_url, headers=headers, course_codes=course_codes, start_date='2025-01-10T10:55:32Z')
#     processed_announcements = app.process_announcements_for_broker(announcements=announcements)
#     for ann in processed_announcements:
#         print('announcements', ann)
#         pubsub_publisher.publish_message("canvas", ann)
#     new_date = app.get_new_date()
#     redis.set('canvas_last_time', new_date)
#     time.sleep(3600)

from canvas import CanvasFirst, Modules, Submissions, Assignments, Database, KeyEncryptor, convert_to_markdown, analyze
from pydantic import BaseModel
from typing import Optional
db = Database()

class RequestHandler(BaseModel):
    email: Optional[str] = None
    api_key: Optional[str] = None

import threading
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signin")
def login(value: RequestHandler):
    email = value.email
    api_key = value.api_key
    user = db.get_user(email=email)
    if not user:
        return {"error": "Could not login user"}
    if KeyEncryptor.decrypt(user['api_key']) != api_key:
        return {"error": "Could not login user"}
    return {"email": email, "api_key": user['api_key'], "success": True}

@app.post("/register")
def register(value: RequestHandler):
    email = value.email
    api_key = value.api_key
    user = db.get_user(email=email)
    if user:
        return {"error": "Could not register user"}
    else:
        user_canvas = CanvasFirst(api_key=api_key, email=email)
        user_info = user_canvas.get_user_and_courses()
        db.add_user(user_info)
        api_key = KeyEncryptor.decrypt(user_info['api_key'])
        email = user_info['email']
        def populate():
            for course in user_info['courses']:
                
                # add modules
                modules = Modules(course_id= course['course_id'], api_key=api_key)

                all_modules = modules.get_modules()
                for j in range(len((all_modules))):
                    module_items = all_modules[j]['module_items']
                    for i in range(len(module_items)):
                        item_markdown = convert_to_markdown(module_items[i]['module_item_download_url'])
                        analysis = analyze(item_markdown)
                        all_modules[j]['module_items'][i]['module_item_analysis'] = analysis
                        all_modules[j]['module_items'][i]['module_item_markdown'] = item_markdown
                for module in all_modules:
                    module_items = module.pop('module_items')
                    db.add_module(module)
                    for module_item in module_items:
                        db.add_module_item(module_item)
                # add assignments
                assignments = Assignments(course_id= course['course_id'], api_key=api_key)
                all_assignments = assignments.get_assignments()
                for assignment in all_assignments:
                    db.add_assignment(assignment)
        thread = threading.Thread(target=populate)
        thread.start()
        return {"status": "User registered successfully", "success": True}
    return {"error": "Could not register user"}


@app.get("/courses")
def get_courses(email: str):
    user_info = db.get_user(email=email)
    if not user_info:
        return {"error": "Could not login user"}
    user_courses = user_info['courses']
    for course in user_courses:
        course['course_id'] = str(course['course_id'])
    return {"courses": user_courses}

@app.get("/courses/{course_id}")
def get_course(course_id: str, email: str):
    user_info = db.get_user(email=email)
    if not user_info:
        return {"error": "Could not login user"}
    courses = user_info['courses']
    for course in courses:
        course['course_id'] = str(course['course_id'])
        if course['course_id'] == course_id:
            return {"course": course}
    return {"error": "Course not found"}

@app.get("/courses/{course_id}/modules")
def get_modules(course_id: str, email: str):
    modules = db.get_modules(course_id=course_id)
    return {"modules": modules}

@app.get("/courses/{course_id}/modules/{module_id}")
def get_module(course_id: str, module_id: str):
    module = db.get_module(course_id=course_id, module_id=module_id)
    return {"module": module}

@app.get("/modules/{module_id}/moduleitems")
def get_module_items(module_id: str):
    module_items = db.get_module_items(module_item_module_id=module_id)
    return {"module_items": module_items}

@app.get("/modules/{module_id}/moduleitems/{module_item_id}")
def get_module_item(module_id: str, module_item_id: str):
    module_item = db.get_module_item(module_item_module_id=module_id, module_item_id=module_item_id)
    return {"module_item": module_item}

@app.get("/courses/{course_id}/assignments")
def get_assignments(course_id: str):
    assignments = db.get_assignments(course_id=course_id)
    return {"assignments": assignments}
    
@app.get("/courses/{course_id}/assignments/{assignment_id}")
def get_assignment(assignment_id: str, course_id: str):
    assignment = db.get_assignment(assignment_id=assignment_id, course_id=course_id)
    return {"assignment": assignment}