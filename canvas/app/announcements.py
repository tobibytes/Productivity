import requests
from typing import List

def get_announcements_from_canvas(canvas_url: str, start_date: str, course_codes: List[str], headers: dict):
    try:
        url = f"{canvas_url}?start_date={start_date}&{course_codes}"
        data = requests.get(url=url, headers=headers)
        return data.json()
    except Exception as e:
        print(e)
        return None