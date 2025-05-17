data = {
    "event": "start_note_summary",
    "course_id": "131540000000042861",
    "module_id": "296810",
    "module_item_id": "6271689",
    "email": "olola73@morgan.edu"
}

import redis
r = redis.Redis(host="localhost", port="6379", decode_responses=True)


r.xadd( "ai.tasks", data)
# print(r.keys())
