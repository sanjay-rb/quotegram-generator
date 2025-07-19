import json
import os
import requests
from dotenv import load_dotenv

from const import (
    DEFAULT_QUOTE,
    FILE_HASHTAG_TODAY,
    FILE_QUOTE_TODAY,
    FILE_MOTIVATION_TODAY,
)

# Load environment variables
load_dotenv()

# --- Configuration ---
bot_token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_TO"]  # e.g., 123456789


def generate_telegram_message(quote_data):
    try:
        quote = quote_data.get("q", DEFAULT_QUOTE["q"])
        author = quote_data.get("a", DEFAULT_QUOTE["a"])
        print(f"Generating telegram message: {quote} - {author}")

        with open(FILE_HASHTAG_TODAY, "r") as f:
            hashtags = f.read().strip()
        caption_text = f"""{quote}
    - {author}
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
        with open(FILE_MOTIVATION_TODAY, "rb") as video_file:
            url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
            files = {"video": video_file}
            data = {
                "chat_id": chat_id,
                "caption": caption_text,
                "parse_mode": "HTML",  # or 'MarkdownV2'
            }

            response = requests.post(url, data=data, files=files)
            response.raise_for_status()

            return response.json()
    except Exception as e:
        print(f"Error generating telegram message: {e}")
        return None


def main():
    with open(FILE_QUOTE_TODAY, "r") as f:
        quote_data = json.load(f)

    caption = generate_telegram_message(quote_data)
    print("Generated telegram message:", caption)


if __name__ == "__main__":
    main()
