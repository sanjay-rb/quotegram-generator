import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration ---
bot_token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_TO"]  # e.g., 123456789
video_path = os.environ["FILE_MOTIVATION_TODAY"]


def send_video_to_telegram(quote=""):
    with open(os.environ["FILE_HASHTAG_TODAY"], "r") as f:
        hashtags = f.read().strip()
    caption_text = f"""{quote}
.
.
.
.
.
.
.
.
.
.
.
.
{hashtags}
"""
    # --- Send the video ---
    with open(video_path, "rb") as video_file:
        url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
        files = {"video": video_file}
        data = {
            "chat_id": chat_id,
            "caption": caption_text,
            "parse_mode": "HTML",  # or 'MarkdownV2'
        }

        response = requests.post(url, data=data, files=files)
        print(response.status_code)
        print(response.text)

        if response.ok:
            print("✅ Video sent successfully!")
        else:
            print("❌ Failed to send video.")


if __name__ == "__main__":

    quote = "Bitterness is like a cancer that enters the soul."
    send_video_to_telegram(quote)
