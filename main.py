from fastapi import FastAPI, Form, HTTPException
from transcript_fetcher import fetch_transcript

app = FastAPI(title="YouTube Transcript API")


@app.get("/")
def home():
    return {"message": "Transcript API Running on Render 🚀"}


@app.post("/fetch_transcript")
async def get_transcript(url: str = Form(...)):
    try:
        return fetch_transcript(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
