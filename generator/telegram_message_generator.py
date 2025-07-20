import json
import os
import requests
from dotenv import load_dotenv

from const import *


def generate_telegram_message(quote_data):
    try:
        # Load environment variables
        load_dotenv()

        # --- Configuration ---
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]  # e.g., 123456789

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating telegram message: {quote} - {author}")

        with open(OUT_HASHTAGS_TODAY_FILE, "r") as f:
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
        with open(OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT, "rb") as video_file:
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
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    caption = generate_telegram_message(quote_data)
    if caption:
        print("Generated telegram message:", caption)
    else:
        raise RuntimeError("Failed to generate telegram message.")


if __name__ == "__main__":
    main()
