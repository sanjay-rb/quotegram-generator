"""
Upload a generated video to YouTube Shorts.

This module authenticates with the YouTube Data API v3, uploads a video
as a Short, sets a custom thumbnail, and returns the resulting Shorts URL.
"""

import logging
import os
import time
from typing import Final

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


YOUTUBE_UPLOAD_SCOPE: Final = "https://www.googleapis.com/auth/youtube.upload"
TOKEN_URI: Final = "https://oauth2.googleapis.com/token"
PROCESSING_DELAY_SECONDS: Final = 5


def upload_youtube_short(
    video_path: str,
    thumbnail_path: str,
    youtube_title: str,
    youtube_description: str,
) -> str:
    """Upload a YouTube Short video and set its thumbnail.

    Args:
        video_path: Path to the MP4 video file.
        thumbnail_path: Path to the thumbnail image.
        youtube_title: Title of the YouTube Short.
        youtube_description: Description of the YouTube Short.

    Returns:
        URL of the uploaded YouTube Short.
    """
    load_dotenv()

    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if not all((client_id, client_secret, refresh_token)):
        raise RuntimeError("Missing required YouTube API credentials")

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=client_id,
        client_secret=client_secret,
        scopes=[YOUTUBE_UPLOAD_SCOPE],
    )

    youtube = build("youtube", "v3", credentials=credentials)

    upload_request = youtube.videos().insert(  # pylint: disable=no-member
        part="snippet,status",
        body={
            "snippet": {
                "title": youtube_title,
                "description": youtube_description,
                "tags": ["shorts"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public"},
        },
        media_body=MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            resumable=True,
        ),
    )

    response = upload_request.execute()
    video_id = response["id"]
    logging.info("Uploaded video with ID: %s", video_id)

    logging.info(
        "Waiting %s seconds for YouTube to process video before "
        "setting thumbnail...",
        PROCESSING_DELAY_SECONDS,
    )
    time.sleep(PROCESSING_DELAY_SECONDS)

    thumb_request = youtube.thumbnails().set(  # pylint: disable=no-member
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path, resumable=False),
    )
    thumb_response = thumb_request.execute()
    logging.info("Thumbnail set successfully: %s", thumb_response)

    return f"https://www.youtube.com/shorts/{video_id}"
