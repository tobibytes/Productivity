import app
import time
pubsub_publisher = app.PubSub('redis')
redis = app.get_redis('redis')
time.sleep(5)
while True:
    start_date = app.get_start_date(redis)
    course_codes = app.process_context_codes_for_url(app.Config.COURSES_ID)
    headers = app.Config.CANVAS_HEADERS
    canvas_url = app.Config.CANVAS_API_URL
    announcements= app.get_announcements_from_canvas(canvas_url=canvas_url, headers=headers, course_codes=course_codes, start_date='2025-01-10T10:55:32Z')
    processed_announcements = app.process_announcements_for_broker(announcements=announcements)
    for ann in processed_announcements:
        print('announcements', ann)
        pubsub_publisher.publish_message("canvas", ann)
    new_date = app.get_new_date()
    redis.set('canvas_last_time', new_date)
    time.sleep(3600)
