import logging
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

from common.constants import (
    IMAGE_GENERATION_MODEL,
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT,
    PROMPT_IMAGE_GENERATION_TEMPLATE,
)
from generator.text_generator import generate_visual_theme


def generate_image(quote_data: dict) -> str:
    load_dotenv()

    # Step 1: Generate quote-relevant visual theme
    visual_theme = generate_visual_theme(quote_data)

    # Step 2: Create FLUX background
    client = InferenceClient(IMAGE_GENERATION_MODEL, token=os.environ["HF_TOKEN"])

    with open(PROMPT_IMAGE_GENERATION_TEMPLATE, "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.format(visual_theme=visual_theme)

    logging.info(f"Generating FLUX background with theme: {visual_theme}")
    image = client.text_to_image(prompt=prompt)
    image.save(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)
    logging.info(f"Background saved: {OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT}")
    return OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT
