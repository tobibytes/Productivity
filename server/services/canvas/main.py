import canvas

redis = canvas.get_redis(canvas.Config.REDIS_URL)

start_date = canvas.get_start_date()
course_codes = canvas.process_context_codes_for_url()
headers = canvas.Config.CANVAS_HEADERS
canvas_url = canvas.Config.CANVAS_API_URL
announcements= canvas.get_announcements_from_canvas(canvas_url=canvas_url, headers=headers, course_codes=course_codes, start_date=start_date)
canvas.process_announcements_for_kafka(announcments=announcements)
new_date = canvas.get_new_date()