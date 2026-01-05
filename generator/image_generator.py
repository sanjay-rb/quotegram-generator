import json
import os
import random
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


def generate_image_from_quote(quote_data: dict) -> str:
    try:
        load_dotenv()

        OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")

        client = InferenceClient(
            provider="hf-inference",
            api_key=os.environ["HF_TOKEN"],
        )

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        prompt = f"""Goal: Create an inspirational, cinematic modern artwork visually inspired by the meaning and emotion of {quote} by {author}, without displaying any text.
Context: Translate the quote's theme into visual form using a high-end ArtStation aesthetic, rendered in 4K with vibrant colors, cinematic lighting, and a modern art style. Preserve intentional negative space in the top area and left corner.
Deliverable: One high-quality, highly detailed digital artwork with rich colors, cinematic atmosphere, polished finish, and clear negative space in the top and left areas.
Guardrails: No text, no quote, no author name, no words, no letters, no numbers, no watermarks, no logos, no signatures, no emojis, no symbols, no characters. Avoid clutter, blur, noise, artifacts, flat lighting, dull colors, cartoon or outdated styles.
Autonomy: Freely choose visual elements, composition, lighting, and color palette while strictly following all constraints.
Self-Check: Ensure the artwork conveys the quote's spirit without text, is cinematic and modern, meets 4K quality, keeps the top and left areas visually clear, and contains no forbidden elements."""
        print(f"Generating image for prompt: {prompt}")

        # Generate image using the text-to-image model
        models = [
            "black-forest-labs/FLUX.1-dev",
            # "stabilityai/stable-diffusion-xl-base-1.0",
            "black-forest-labs/FLUX.1-schnell",
            # "stabilityai/stable-diffusion-3-medium-diffusers",
        ]
        image = client.text_to_image(
            prompt=prompt,
            model=random.choice(models),
        )
        image.save(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)
        print(f"Image saved to {OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT}")
        return OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def main():
    load_dotenv()
    OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    image_path = generate_image_from_quote(quote_data)
    if image_path:
        print("Generated image:", image_path)
    else:
        raise RuntimeError("Failed to generate image.")


if __name__ == "__main__":
    main()
