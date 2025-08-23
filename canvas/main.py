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

from canvas import CanvasFirst, Modules, Submissions, Assignments, Database, KeyEncryptor, convert_to_markdown
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import redis
import uuid
import os
import time
import jwt
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

r = redis.Redis(host='redis', port=6379)
load_dotenv()
db = Database()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-secret-change-me")
JWT_ALG = "HS256"
SESSION_COOKIE_NAME = "session"
SESSION_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
SESSION_COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax").lower()
SESSION_COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", None)

class RequestHandler(BaseModel):
    email: Optional[str] = None
    api_key: Optional[str] = None

class SuscribeToPricing(BaseModel):
    email: str
    pricing_id: Optional[str] = None

import threading

app = FastAPI()
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simple Redis-based rate limiting ---
from functools import wraps

def rate_limit(key_prefix: str, limit: int, window_sec: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request: Request = kwargs.get("request") or next((a for a in args if isinstance(a, Request)), None)
                ip = request.client.host if request else "unknown"
                key = f"ratelimit:{key_prefix}:{ip}"
                current = r.incr(key)
                if current == 1:
                    r.expire(key, window_sec)
                if current > limit:
                    raise HTTPException(status_code=429, detail="Too Many Requests")
            except Exception:
                # Fail open if redis is not available
                pass
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.get("/")
def read_root():
    return {"Hello": "World"}

# --- Auth helpers ---

def create_jwt(email: str) -> str:
    return jwt.encode({"email": email, "iat": int(time.time())}, JWT_SECRET, algorithm=JWT_ALG)

def get_email_from_request(request: Request) -> Optional[str]:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload.get("email")
    except Exception:
        return None

# --- Auth endpoints ---
class MeResponse(BaseModel):
    email: str

@app.get("/auth/me")
def auth_me(request: Request):
    email = get_email_from_request(request)
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"email": email}

@app.post("/auth/logout")
def auth_logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"success": True}

@app.post("/signin")
@rate_limit("signin", limit=10, window_sec=60)
def login(value: RequestHandler, response: Response):
    email = value.email
    api_key = value.api_key
    user = db.get_user(email=email)
    if not user:
        return {"error": "Could not login user"}
    if KeyEncryptor.decrypt(user['api_key']) != api_key:
        return {"error": "Could not login user"}
    # Set signed session cookie
    token = create_jwt(email)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        domain=SESSION_COOKIE_DOMAIN,
        path="/",
    )
    return {"email": email, "success": True}

@app.post("/register")
@rate_limit("register", limit=5, window_sec=300)
def register(value: RequestHandler):
    email = value.email
    api_key = value.api_key
    user = db.get_user(email=email)
    if user:
        return {"error": "Could not register user"}
    else:
        user_canvas = CanvasFirst(api_key=api_key, email=email)
        user_info = user_canvas.get_user_and_courses()
        user_info['pricing_id'] =  None
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
                        try:
                            item_markdown = convert_to_markdown(module_items[i]['module_item_download_url'])
                            all_modules[j]['module_items'][i]['module_item_markdown'] = item_markdown
                        except:
                            all_modules[j]['module_items'][i]['module_item_markdown'] = ""
                            
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

@app.get("/users/{email}")
def get_user(email: str):
    user_info = db.get_user(email=email)
    if not user_info:
        return {"error": "Could not login user"}
    # Never expose decrypted API keys
    if 'api_key' in user_info:
        user_info.pop('api_key')
    return {"user": user_info}


@app.get("/courses")
def get_courses(email: Optional[str] = None, request: Request = None):
    if not email and request is not None:
        email = get_email_from_request(request)
    user_info = db.get_user(email=email)
    if not user_info:
        return {"error": "Could not login user"}
    user_courses = user_info['courses']
    for course in user_courses:
        course['course_id'] = str(course['course_id'])
    return {"courses": user_courses}

@app.get("/courses/{course_id}")
def get_course(course_id: str, email: Optional[str] = None, request: Request = None):
    if not email and request is not None:
        email = get_email_from_request(request)
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

@app.get("/moduleitems/{module_item_id}/note")
def get_note(module_item_id: str, email: Optional[str] = None, request: Request = None):
    if not email and request is not None:
        email = get_email_from_request(request)
    note = db.get_note(module_item_id, email)
    if note:
        return { "note": note["note"]}
    return {"error": "Note not found"}

@app.get("/moduleitems/{module_item_id}/flashcards")
def get_flashcards(module_item_id: str, email: Optional[str] = None, request: Request = None):
    if not email and request is not None:
        email = get_email_from_request(request)
    flashcards = db.get_flashcards(module_item_id, email)
    if flashcards and 'flashcards' in flashcards:
        return {"flashcards": flashcards['flashcards']}
    return {"error": "Flashcards not found"}

import json
import time
class SearchPostRequest(BaseModel):
    course_id: Optional[str] = None
    module_id: Optional[str] = None
    module_item_id: Optional[str] = ''
    email: str
    text: str
    uuid: Optional[str] = None
    event: Optional[str] = None
    
@app.post("/search")
@rate_limit("search", limit=60, window_sec=60)
def search(query: SearchPostRequest):
    course_id = query.course_id
    module_id = query.module_id
    email = query.email
    text = query.text
    if not email or not text or text == "":
        return {"error": "Please provide an email and text"}
    
    query.uuid = str(uuid.uuid4())
    query.event = "search_embedding"
    f_query = query.dict(exclude_unset=True)
    
    r.xadd("ai.tasks", f_query)
    # avoid CPU spin; wait with timeout and small sleep
    waited = 0
    step = 0.05
    timeout = 10
    while r.get(f_query["uuid"]) is None and waited < timeout:
        time.sleep(step)
        waited += step
    result = r.get(f_query["uuid"]) if r.get(f_query["uuid"]) else "[]"
    return {"result": json.loads(result)}
    
    
class N8NPostRequest(BaseModel):
    output: str
    
@app.post("/n8n")
def post_n8n(query: N8NPostRequest):
    print(query.output)
    return {"result": query.output}