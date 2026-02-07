"""
This is the main entry point for the Quotegram project.
It orchestrates the entire process of
- Generating a quote
- Creating the associated media
- Uploading it to YouTube Shorts
- Sending notifications via Telegram.
"""

import logging

from generator.quote_generator import generate_quote
from generator.text_generator import generate_title, generate_description
from generator.image_generator import generate_image
from generator.video_generator import generate_video

from upload.youtube_short_uploader import upload_youtube_short

from messenger.send_message import send_telegram_video, send_telegram_text


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Main function to orchestrate the quotegram generation and distribution."""
    quote = generate_quote()
    logging.info("✅ Generated quote: %s - %s", quote.get("q"), quote.get("a"))

    title = generate_title(quote)
    logging.info("✅ Generated title: %s", title)

    description = generate_description(quote)
    logging.info("✅ Generated description for youtube: %s", description)

    image = generate_image(quote)
    logging.info("✅ Generated image for quotegram: %s", image)

    video = generate_video(quote, image)
    logging.info("✅ Generated video for quotegram: %s", video)

    youtube_url = upload_youtube_short(video, image, title, description)
    logging.info("✅ Uploaded YouTube Short: %s", youtube_url)

    send_telegram_video(video)
    logging.info("✅ Video sent successfully (no caption).")

    send_telegram_text(title)
    logging.info("✅ YouTube title message sent.")

    send_telegram_text(description)
    logging.info("✅ YouTube description message sent.")

    send_telegram_text(youtube_url)
    logging.info("✅ YouTube url message sent.")


if __name__ == "__main__":
    main()
