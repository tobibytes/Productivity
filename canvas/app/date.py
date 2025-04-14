from datetime import datetime, timezone

def get_start_date(cache):
    date = cache.get("canvas_last_time")
    if not date:
        date = get_new_date()
    return date


def get_new_date():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")