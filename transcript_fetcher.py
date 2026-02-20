from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator
import re


def get_video_id(url: str):
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc:
        return parse_qs(parsed.query).get("v", [None])[0]

    elif "youtu.be" in parsed.netloc:
        return parsed.path.strip("/")

    else:
        raise ValueError("Invalid YouTube URL")


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_transcript(video_url: str):

    video_id = get_video_id(video_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        language = "en"
    except:
        transcript = YouTubeTranscriptApi.list_transcripts(video_id)\
            .find_transcript(['hi', 'ur']).fetch()
        language = "other"

    text = " ".join([t["text"] for t in transcript])
    text = clean_text(text)

    if language != "en":
        translator = GoogleTranslator(source="auto", target="en")

        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        text = " ".join(translator.translate(c) for c in chunks)

    return {
        "video_id": video_id,
        "transcript": text
    }
