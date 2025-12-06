import os
from dotenv import load_dotenv
from instagrapi import Client

import subprocess
import sys


# Now you can safely import instagrapi and use clip_upload
from instagrapi import Client


def upload_insta_reel(insta_caption):
    load_dotenv()
    OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT")
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")
    OUT_INSTA_URL_TODAY_FILE = os.getenv("OUT_INSTA_URL_TODAY_FILE")
    INSTA_USERNAME = os.getenv("INSTA_USERNAME")
    INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

    insta_client = Client()

    # Login (first time)
    insta_client.login(INSTA_USERNAME, INSTA_PASSWORD)
    insta_client.dump_settings("insta_settings.json")

    # media = insta_client.clip_upload(
    #     path=OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
    #     caption=insta_caption,
    #     thumbnail=OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT,
    # )
    # with open(OUT_INSTA_URL_TODAY_FILE, "w") as f:
    #     f.write(f"https://www.instagram.com/reel/{media.code}/")

    # return f"https://www.instagram.com/reel/{media.code}/"


def main():
    load_dotenv()
    insta_url = upload_insta_reel()
    if insta_url:
        print("Uploaded to Instagram:", insta_url)
    else:
        raise RuntimeError("Failed to upload to Instagram.")


def main():
    load_dotenv()
    OUT_INSTA_CAPTION_TODAY_FILE = os.getenv("OUT_INSTA_CAPTION_TODAY_FILE")

    # Downgrade moviepy to avoid compatibility issues
    subprocess.run([sys.executable, "-m", "pip", "install", "moviepy==1.0.3"])

    with open(OUT_INSTA_CAPTION_TODAY_FILE, "r") as f:
        insta_caption = f.read().strip()

    youtube_url = upload_insta_reel(insta_caption)
    if youtube_url:
        print("Uploaded to youtube:", youtube_url)
    else:
        raise RuntimeError("Failed to upload youtube.")


if __name__ == "__main__":
    main()
