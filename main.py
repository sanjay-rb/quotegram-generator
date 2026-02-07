from generator.quote_generator import generate_quote
from generator.text_generator import generate_title, generate_description
from generator.image_generator import generate_image
from generator.video_generator import generate_video
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    quote = generate_quote()
    logging.info(f"Generated quote: {quote.get('q')} - {quote.get('a')}")

    title = generate_title(quote)
    logging.info(f"Generated title: {title}")

    description = generate_description(quote)
    logging.info(f"Generated description for youtube: {description}")

    image = generate_image(quote)
    logging.info(f"Generated image for quotegram: {image}")

    video = generate_video(quote, image)
    logging.info(f"Generated video for quotegram: {video}")


if __name__ == "__main__":
    main()
