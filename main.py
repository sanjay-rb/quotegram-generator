"""
Orchestrate the Quotegram generation and distribution pipeline.

This module coordinates quote generation, media creation, YouTube Shorts
upload, and Telegram notifications.
"""

import logging
import traceback

from generator.image_generator import generate_image
from generator.quote_generator import generate_quote
from generator.text_generator import generate_description, generate_title
from generator.video_generator import generate_video
from messenger.send_message import send_telegram_text, send_telegram_video
from upload.youtube_short_uploader import upload_youtube_short
from common.functions import ask_llm_for_fix


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main() -> None:
    """Run the full Quotegram generation and publishing workflow."""
    quote = generate_quote()
    logging.info("✅Generated quote: %s - %s", quote.get("q"), quote.get("a"))

    title = generate_title(quote)
    if title is None:
        raise RuntimeError("Failed to generate title")
    logging.info("✅ Generated title: %s", title)

    description = generate_description(quote)
    if description is None:
        raise RuntimeError("Failed to generate description")
    logging.info("✅ Generated YouTube description: %s", description)

    image = generate_image(quote)
    logging.info("✅ Generated image: %s", image)

    video = generate_video(quote, image)
    logging.info("✅ Generated video: %s", video)

    youtube_url = upload_youtube_short(video, image, title, description)
    logging.info("✅ Uploaded YouTube Short: %s", youtube_url)

    send_telegram_video(video)
    logging.info("✅ Video sent to Telegram.")

    send_telegram_text(title)
    logging.info("✅ Title message sent to Telegram.")

    send_telegram_text(description)
    logging.info("✅ Description message sent to Telegram.")

    send_telegram_text(youtube_url)
    logging.info("✅ YouTube URL sent to Telegram.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.error("Traceback:\n%s", traceback.format_exc())
        fix_suggestion = ask_llm_for_fix(str(e), traceback.format_exc())
        if fix_suggestion:
            logging.info("LLM Fix Suggestion:\n%s", fix_suggestion)
        else:
            logging.error("Failed to get fix suggestion from LLM")
        raise
