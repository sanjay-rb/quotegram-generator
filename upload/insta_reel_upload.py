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
        sessionid = session_dict.get("authorization_data", {}).get("sessionid")
        if not sessionid:
            raise ValueError("Session ID is missing. Please log in again.")
        cl.login_by_sessionid(sessionid)
        print("✅ Logged in using existing session.")

    except LoginRequired:
        print("⚠️ Session expired. Please log in with username & password...")
        INSTA_USERNAME = os.getenv("INSTA_USERNAME")
        INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)

        # Save fresh session
        cl.dump_settings(INSTA_SESSION_FILE)
        print("✅ New session saved to insta_settings.json")

    except ClientError as e:
        print(f"⚠️ Client error occurred: {e}")
        raise

    except Exception as e:
        print(
            f"⚠️ Session expired or invalid with error: {e}. Logging in with username & password..."
        )
        INSTA_USERNAME = os.getenv("INSTA_USERNAME")
        INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
        cl.login(INSTA_USERNAME, INSTA_PASSWORD)

        # Save fresh session
        cl.dump_settings(INSTA_SESSION_FILE)
        print("✅ New session saved to insta_settings.json")

    # Now upload your reel safely
    if not os.path.exists(OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT):
        raise FileNotFoundError(
            f"Video file not found: {OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT}"
        )
    if not os.path.exists(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT):
        print(f"Warning: Thumbnail file not found: {OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT}")
        thumbnail = None
    else:
        thumbnail = OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT

    try:
        media = cl.clip_upload(
            path=OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
            caption=insta_caption,
        )
        with open(OUT_INSTA_URL_TODAY_FILE, "w") as f:
            f.write(f"https://www.instagram.com/reel/{media.code}/")

        return f"https://www.instagram.com/reel/{media.code}/"
    except Exception as e:
        error_str = str(e)
        if "'status': 'ok'" in error_str:
            print("⚠️ Upload encountered an error but status is 'ok'. Assuming success.")
            # Since we don't have media.code, write a placeholder or skip
            with open(OUT_INSTA_URL_TODAY_FILE, "w") as f:
                f.write("https://www.instagram.com/reel/unknown/")  # Placeholder
            return "https://www.instagram.com/reel/unknown/"
        else:
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
