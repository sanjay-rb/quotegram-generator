import json
import os
import re
import traceback
from openai import OpenAI
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


def generate_visual_theme(quote_data: dict) -> str:
    """
    Standalone function: Converts quote into ONE visual background theme using LLM.
    Returns clean visual description for FLUX background generation.
    """
    try:
        load_dotenv()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPEN_ROUTER_API_KEY"],
        )

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))
        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])

        prompt = f"""
        **Instruction:**

You are a theme generator.
Given a quote and its author, produce a **background theme description** in **5–12 words** that captures the **mood and emotional tone**.

Rules:

* Do **not** describe a specific image
* Do **not** include the quote text or author name
* No punctuation
* Return **only** the theme text

---

**Examples:**

Quote: “The only way out is through” — Robert Frost
Theme: resilience through struggle and quiet determination

Quote: “Happiness depends upon ourselves” — Aristotle
Theme: inner peace and mindful self awareness

Quote: “In the middle of difficulty lies opportunity” — Albert Einstein
Theme: optimism emerging from challenge and uncertainty

Quote: “Not all those who wander are lost” — J R R Tolkien
Theme: freedom curiosity and purposeful exploration

---

**Now generate a theme for:**

Quote: “{quote}” — {author}
Theme:
"""

        print(f"Extracting visual theme from: {quote[:50]}...")
        completion = client.chat.completions.create(
            extra_body={"reasoning": {"enabled": True}},
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
        )

        output = completion.choices[0].message.content.strip()
        print(f"Generated visual theme: '{output}'")
        return str(output)

    except Exception as e:
        print(f"Error in theme generation: {e}")
        traceback.print_exc()
        return "serene mountain lake reflecting golden sunset clouds"


def generate_image_from_quote(quote_data: dict) -> str:
    try:
        load_dotenv()
        OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")

        # Step 1: Generate quote-relevant visual theme
        visual_theme = generate_visual_theme(quote_data)

        # Step 2: Create FLUX background
        client = InferenceClient(
            "black-forest-labs/FLUX.1-dev",
            token=os.environ["HF_TOKEN"],
        )

        background_prompt = (
            f"{visual_theme}, cinematic abstract background, "
            "vibrant cinematic colors, 4k ultra detailed, modern artstation, "
            "soft dramatic lighting, atmospheric gradients, subtle texture, "
            "large clean empty space at top third and left third, "
            "purely visual atmospheric scene, completely text-free, "
            "no words, no letters, no numbers, no logos, no watermarks, "
            "no UI, no icons, no symbols, no text anywhere"
        )

        print(f"Generating FLUX background with theme: {visual_theme}")
        image = client.text_to_image(prompt=background_prompt)
        image.save(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)
        print(f"Background saved: {OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT}")
        return OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT

    except Exception as e:
        print(f"Error generating image: {e}")
        traceback.print_exc()
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
