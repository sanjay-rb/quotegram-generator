import json
import os
import requests
from dotenv import load_dotenv


def send_telegram_video(bot_token, chat_id, video_path):
    """Send a video (no caption) to Telegram."""
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        data = {"chat_id": chat_id}
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        return response.json()


def send_telegram_text(bot_token, chat_id, text):
    """Send a text message to Telegram."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()


def generate_telegram_message(quote_data):
    try:
        # Load environment variables
        load_dotenv()
        OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT")
        OUT_YOUTUBE_TITLE_TODAY_FILE = os.getenv("OUT_YOUTUBE_TITLE_TODAY_FILE")
        OUT_INSTA_CAPTION_TODAY_FILE = os.getenv("OUT_INSTA_CAPTION_TODAY_FILE")
        OUT_YOUTUBE_URL_TODAY_FILE = os.getenv("OUT_YOUTUBE_URL_TODAY_FILE")
        OUT_INSTA_URL_TODAY_FILE = os.getenv("OUT_INSTA_URL_TODAY_FILE")

        # --- Configuration ---
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))
        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating telegram message: {quote} - {author}")

        # --- Send the video (no caption) ---
        send_telegram_video(bot_token, chat_id, OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT)
        print("✅ Video sent successfully (no caption).")

        # --- Send youtube title message ---
        with open(OUT_YOUTUBE_TITLE_TODAY_FILE, "r") as f:
            youtube_title = f.read().strip()
            send_telegram_text(bot_token, chat_id, youtube_title)
            print("✅ YouTube title message sent.")

        # --- Send insta caption message ---
        with open(OUT_INSTA_CAPTION_TODAY_FILE, "r") as f:
            insta_caption = f.read().strip()
            send_telegram_text(bot_token, chat_id, insta_caption)
            print("✅ Instagram caption message sent.")

        # --- Send youtube url message ---
        with open(OUT_YOUTUBE_URL_TODAY_FILE, "r") as f:
            youtube_url = f.read().strip()
            send_telegram_text(bot_token, chat_id, youtube_url)
            print("✅ YouTube url message sent.")

        # # --- Send instagram url message ---
        # with open(OUT_INSTA_URL_TODAY_FILE, "r") as f:
        #     insta_url = f.read().strip()
        #     send_telegram_text(bot_token, chat_id, insta_url)
        #     print("✅ Instagram url message sent.")

        return True

    except Exception as e:
        print(f"❌ Error generating telegram message: {e}")
        return False


def main():
    load_dotenv()
    OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    success = generate_telegram_message(quote_data)
    if success:
        print("All Telegram messages sent successfully.")
    else:
        raise RuntimeError("Failed to send Telegram messages.")


if __name__ == "__main__":
    main()
