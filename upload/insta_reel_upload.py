import os
import subprocess
import sys
from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError


def upload_insta_reel(insta_caption):
    load_dotenv()
    OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT")
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")
    OUT_INSTA_URL_TODAY_FILE = os.getenv("OUT_INSTA_URL_TODAY_FILE")
    INSTA_SESSION_FILE = os.getenv("INSTA_SESSION_FILE", "insta_settings.json")

    cl = Client()

    try:
        # Try loading and using the old session
        session_dict = cl.load_settings(INSTA_SESSION_FILE)
        sessionid = session_dict.get("authorization_data").get("sessionid")
        cl.login_by_sessionid(sessionid)
        print("✅ Logged in using existing session.")

    except Exception as e:
        print(
            f"⚠️ Session expired with error {e}. Logging in with username & password..."
        )
        # # raise ValueError("Session expired. Please re-login manually.")

        # # Uncomment below code for Login normally
        # INSTA_USERNAME = os.getenv("INSTA_USERNAME")
        # INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
        # cl = Client()
        # cl.login(INSTA_USERNAME, INSTA_PASSWORD)

        # # Save fresh session
        # cl.dump_settings(INSTA_SESSION_FILE)
        # print("✅ New session saved to insta_settings.json")

    # Now upload your reel safely
    try:
        media = cl.clip_upload(
            path=OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
            caption=insta_caption,
            thumbnail=OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT,
        )
        with open(OUT_INSTA_URL_TODAY_FILE, "w") as f:
            f.write(f"https://www.instagram.com/reel/{media.code}/")

        return f"https://www.instagram.com/reel/{media.code}/"
    except Exception as e:
        print("❌ Upload failed:", e)


def main():
    load_dotenv()
    OUT_INSTA_CAPTION_TODAY_FILE = os.getenv("OUT_INSTA_CAPTION_TODAY_FILE")

    # Downgrade moviepy to avoid compatibility issues
    # subprocess.run([sys.executable, "-m", "pip", "install", "moviepy==1.0.3"])

    with open(OUT_INSTA_CAPTION_TODAY_FILE, "r") as f:
        insta_caption = f.read().strip()

    insta_url = upload_insta_reel(insta_caption)
    if insta_url:
        print("Uploaded to instagram:", insta_url)
    else:
        raise RuntimeError("Failed to upload instagram.")


if __name__ == "__main__":
    main()
