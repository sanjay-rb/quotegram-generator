import json
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from const import *

load_dotenv()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["HF_TOKEN_2"],
)


def generate_image_from_quote(quote_data: dict) -> str:
    try:
        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        prompt = f"{quote} - {author}, inspirational, cinematic, trending on artstation, 4k, Make sure that you keep space on top & left corner empty. Expected result in high quality, detailed, vibrant colors, modern art style"
        print(f"Generating image for prompt: {prompt}")

        # Generate image using the text-to-image model
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
        )
        image.save(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)
        print(f"Image saved to {OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT}")
        return OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def main():
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    image_path = generate_image_from_quote(quote_data)
    if image_path:
        print("Generated image:", image_path)
    else:
        raise RuntimeError("Failed to generate image.")


if __name__ == "__main__":
    main()
