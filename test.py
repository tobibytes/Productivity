from redis import Redis

r = Redis(host='localhost', port=6379)


# print(r.xadd("ai.tasks", {
#     "event": "search_embedding",
#     "course_id": "131540000000042861",
#     "module_id": "295320",
#     "module_item_id": "6144829",
#     "email": "olola73@morgan.edu",
#     "text": "what keys must be turned simultaneously to start a car?",
#     "uuid": "1234567890"
# }))

# print(r.hgetall('doc:6346252;notes:0;email:olola73@morgan.edu'))
# print(r.get("1234567890"))
print(r.get("1234567890:metadata"))

# def escape_tag(value: str) -> str:
#     return value.replace('@', r'\@').replace(' ', r'\ ')

# print(escape_tag("olola73@morgan.edu"))