import os

class Config:
    CANVAS_API_URL = "https://canvas.instructure.com/api/v1/announcements"
    POSTGRES_URL=""
    KAFKA_URL=""
    REDIS_URL=""
    CANVAS_API_KEY=""
    CANVAS_HEADERS= {
        "Authorization": f"Bearer {os.getenv('CANVAS_ACCESS_TOKEN')}"
    }
    COURSES_ID = []