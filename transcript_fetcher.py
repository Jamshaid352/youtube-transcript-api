from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator
import re


# -----------------------------
# Extract Video ID
# -----------------------------
def get_video_id(url: str):
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]

    elif "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    else:
        raise ValueError("Invalid YouTube URL")


# -----------------------------
# Clean text
# -----------------------------
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Fetch Transcript (NEW SAFE WAY)
# -----------------------------
def fetch_transcript(video_url: str):

    video_id = get_video_id(video_url)

    # Try English first
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en"]
        )
        language = "en"

    # fallback → auto language
    except:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        language = "auto"

    text = " ".join([t["text"] for t in transcript])
    text = clean_text(text)

    # Translate if not English
    if language != "en":
        translator = GoogleTranslator(source="auto", target="en")

        chunks = [
            text[i:i + 4000]
            for i in range(0, len(text), 4000)
        ]

        translated = [
            translator.translate(chunk)
            for chunk in chunks
        ]

        text = " ".join(translated)

    return {
        "video_id": video_id,
        "language": language,
        "transcript": text
    }
