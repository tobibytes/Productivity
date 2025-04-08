import os

class Config:
    CANVAS_API_URL = "https://canvas.instructure.com/api/v1/announcements"
    # POSTGRES_URL="postgresql://admin"
    # KAFKA_URL=""
    REDIS_URL="redis"
    CANVAS_API_KEY="13154~JerZ2enk78z7wwRue29ZGcy4BhXVDQx7CWcFaMNTetT7E9uADWfyWPWEQ36rQAzf"
    CANVAS_HEADERS= {
        "Authorization": f"Bearer {os.getenv('CANVAS_ACCESS_TOKEN')}"
    }
    COURSES_ID = ["131540000000041402", "131540000000042861", "131540000000043180"]