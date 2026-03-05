from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("sk_vxbVvJMLNHNc7kmK38tGCAit_r-c0QfNLbs-7qj13Xc")

TRANSCRIPT_API = "https://transcriptapi.com/api/v2/youtube/transcript"


@app.route("/transcript", methods=["POST"])
def get_transcript():

    data = request.get_json()
    video_id = data.get("video_id")

    params = {
        "video_url": video_id,
        "format": "json"
    }

    headers = {
        "Authorization": "Bearer " + API_KEY
    }

    r = requests.get(
        TRANSCRIPT_API,
        params=params,
        headers=headers,
        timeout=30
    )

    return jsonify(r.json())


@app.route("/")
def home():
    return {"message": "Transcript API Running"}
