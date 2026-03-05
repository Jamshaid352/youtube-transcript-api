from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_KEY = os.getenv(
    "API_KEY",
    "sk_vxbVvJMLNHNc7kmK38tGCAit_r-c0QfNLbs-7qj13Xc"
)

URL = "https://transcriptapi.com/api/v2/youtube/transcript"


@app.get("/")
def home():
    return {"message": "Transcript API running"}


@app.post("/transcript")
def get_transcript(data: dict):

    video_id = data.get("video_id")

    params = {
        "video_url": video_id,
        "format": "json"
    }

    headers = {
        "Authorization": "Bearer " + API_KEY
    }

    r = requests.get(
        URL,
        params=params,
        headers=headers,
        timeout=30
    )

    return r.json()
