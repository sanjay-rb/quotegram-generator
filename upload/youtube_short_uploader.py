import logging
import time
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

from common.constants import (
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT,
    OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
    OUT_YOUTUBE_URL_TODAY_FILE,
)


def upload_youtube_short(youtube_title):
    """Uploads a YouTube Short video and sets its thumbnail."""
    # Load environment variables

    load_dotenv()
    CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )

    youtube = build("youtube", "v3", credentials=creds)

    # -------------------------------------
    # 1. Upload Short
    # -------------------------------------
    upload_request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": youtube_title,
                "description": youtube_title,
                "tags": ["shorts"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public"},
        },
        media_body=MediaFileUpload(
            OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
            resumable=True,
        ),
    )

    response = upload_request.execute()
    video_id = response["id"]
    logging.info("Uploaded Video: %s", video_id)

    # -------------------------------------
    # 2. Set Thumbnail
    # -------------------------------------

    # Wait for processing (3–5 seconds)
    logging.info("Waiting for YouTube to process video before setting thumbnail...")
    time.sleep(5)

    thumbnail_file = OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT
    thumb_request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(
            thumbnail_file, resumable=False
        ),  # resumable must be False
    )
    thumb_response = thumb_request.execute()
    logging.info("Thumbnail set! %s", thumb_response)
    with open(OUT_YOUTUBE_URL_TODAY_FILE, "w") as f:
        f.write("https://www.youtube.com/shorts/" + video_id)
    return "https://www.youtube.com/shorts/" + video_id
