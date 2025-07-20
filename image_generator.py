import json
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from const import DEFAULT_QUOTE, FILE_QUOTE_TODAY, FILE_IMAGE_TODAY

load_dotenv()

client = InferenceClient(
    provider="together",
    api_key=os.environ["HF_TOKEN"],
)


def generate_image_from_quote(quote_data: dict) -> str:
    quote = quote_data.get("q", DEFAULT_QUOTE["q"])
    author = quote_data.get("a", DEFAULT_QUOTE["a"])
    prompt = f"{quote} - {author}, inspirational, cinematic, trending on artstation, 4k, please make sure to include exact string '{quote} - {author}' in the image, high quality, detailed, vibrant colors, modern art style"
    print(f"Generating image for prompt: {prompt}")

    try:
        # Generate image using the text-to-image model
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
        )
        image.save(FILE_IMAGE_TODAY)
        print(f"Image saved to {FILE_IMAGE_TODAY}")
        return FILE_IMAGE_TODAY
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def main():
    with open(FILE_QUOTE_TODAY, "r") as f:
        quote_data = json.load(f)

    image_path = generate_image_from_quote(quote_data)
    if image_path:
        print("Generated image:", image_path)
    else:
        raise RuntimeError("Failed to generate image.")


if __name__ == "__main__":
    main()
