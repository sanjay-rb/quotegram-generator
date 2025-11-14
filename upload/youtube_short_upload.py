from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

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
            "title": "My YouTube Short",
            "description": "Uploaded via GitHub Actions",
            "tags": ["shorts"],
            "categoryId": "22",
        },
        "status": {"privacyStatus": "public"},
    },
    media_body=MediaFileUpload(
        "/Users/sanjayrb/projects/quotegram-generator/output/quotegram_video.mp4",
        resumable=True,
    ),
)

response = upload_request.execute()
video_id = response["id"]
print("Uploaded Video:", video_id)

# -------------------------------------
# 2. Set Thumbnail
# -------------------------------------
thumbnail_file = (
    "/Users/sanjayrb/projects/quotegram-generator/output/quotegram_image.png"
)

thumb_request = youtube.thumbnails().set(
    videoId=video_id, media_body=MediaFileUpload(thumbnail_file)
)

thumb_response = thumb_request.execute()
print("Thumbnail set!")
