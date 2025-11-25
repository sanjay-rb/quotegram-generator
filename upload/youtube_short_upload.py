import json
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


def upload_youtube_short(youtube_title, insta_caption):
    """Uploads a YouTube Short video and sets its thumbnail."""
    # Load environment variables

    load_dotenv()
    OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT")
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")
    OUT_YOUTUBE_URL_TODAY_FILE = os.getenv("OUT_YOUTUBE_URL_TODAY_FILE")

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
                "description": insta_caption,
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
    print("Uploaded Video:", video_id)

    # -------------------------------------
    # 2. Set Thumbnail
    # -------------------------------------
    thumbnail_file = OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT

    thumb_request = youtube.thumbnails().set(
        videoId=video_id, media_body=MediaFileUpload(thumbnail_file)
    )

    thumb_response = thumb_request.execute()
    print(f"Thumbnail set! {thumb_response}")
    with open(OUT_YOUTUBE_URL_TODAY_FILE, "w") as f:
        f.write("https://www.youtube.com/shorts/" + video_id)
    return "https://www.youtube.com/shorts/" + video_id


def main():
    load_dotenv()
    OUT_YOUTUBE_TITLE_TODAY_FILE = os.getenv("OUT_YOUTUBE_TITLE_TODAY_FILE")
    OUT_INSTA_CAPTION_TODAY_FILE = os.getenv("OUT_INSTA_CAPTION_TODAY_FILE")
    with open(OUT_YOUTUBE_TITLE_TODAY_FILE, "r") as f:
        youtube_title = f.read().strip()

    with open(OUT_INSTA_CAPTION_TODAY_FILE, "r") as f:
        insta_caption = f.read().strip()

    youtube_url = upload_youtube_short(youtube_title, insta_caption)
    if youtube_url:
        print("Uploaded to youtube:", youtube_url)
    else:
        raise RuntimeError("Failed to upload youtube.")


if __name__ == "__main__":
    main()
