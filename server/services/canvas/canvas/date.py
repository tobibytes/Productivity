from datetime import datetime

def get_start_date(cache):
    date = cache.get("canvas_last_announcement")
    if not date:
        date = None
    return date

def get_new_date():
    date = datetime.date()
    return date