from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_summary_from_db



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def index():
    return {"hello": "world"}


@app.get('/summary/')
def get_summary():
    summaries = get_summary_from_db()
    return summaries