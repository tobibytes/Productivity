from typing import List
import json
import html2text
def process_announcements_for_broker(announcements : List[dict]):
    try:
        announcments_to_save = []
        for announcement in announcements:
            result = process_announcment_for_broker(announcement)
            announcments_to_save.append(result)
        return announcments_to_save
    except Exception as e:
        print(e)
        return None


def process_announcment_for_broker(announcement : dict):
    try:
        return json.dumps({
            "title": announcement.get('title', None),
            "created_at": announcement.get('created_at', None),
            "url": announcement.get('url', None),
            "context_code": announcement.get('context_code', None),
            "message": html2text.html2text(announcement.get('message', '').strip('\\n')),
            "todo_date": announcement.get('todo_date')
        })
    
    except Exception as e:
        print(e)
        return None

def process_context_codes_for_url(context_codes: List[str]):
    codes = []
    for code in context_codes:
        codes.append(f"context_codes[]=course_{code}")
    return '&'.join(codes)
