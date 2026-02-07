import os
from dotenv import load_dotenv
import requests

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_video(video_path):
    """Send a video (no caption) to Telegram."""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    with open(video_path, "rb") as video_file:
        files = {"video": video_file}
        data = {"chat_id": TELEGRAM_CHAT_ID}
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        return response.json()


def send_telegram_text(text):
    """Send a text message to Telegram."""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()
