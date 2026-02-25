from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator
import re


# -------------------------
# Extract Video ID
# -------------------------
def get_video_id(url):
    parsed_url = urlparse(url)

    if "youtube.com" in parsed_url.netloc:
        return parse_qs(parsed_url.query)["v"][0]

    elif "youtu.be" in parsed_url.netloc:
        return parsed_url.path.strip("/")

    else:
        raise ValueError("Invalid YouTube URL")


# -------------------------
# Clean Text
# -------------------------
def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------
# Fetch + Translate Transcript
# -------------------------
def fetch_transcript(url):

    video_id = get_video_id(url)
    ytt_api = YouTubeTranscriptApi()

    language = "en"

    # Try English first
    try:
        transcript = ytt_api.fetch(video_id, languages=["en"])
        language = "en"

    # fallback → Hindi or any available
    except:
        transcript = ytt_api.fetch(video_id)
        language = transcript.language_code

    text = " ".join([entry.text for entry in transcript])
    text = clean_text(text)

    # Translate if NOT English
    if language != "en":

        translator = GoogleTranslator(
            source="auto",
            target="en"
        )

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
        "original_language": language,
        "transcript": text
    }
