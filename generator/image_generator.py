"""
Generate images for Quotegram content using Hugging Face models.

This module generates a visual background for a quote by creating a
FLUX-style image based on the quote's visual theme.
"""

import logging
import os
from typing import Mapping

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from common.constants import (
    IMAGE_GENERATION_MODEL,
    OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT,
    PROMPT_IMAGE_GENERATION_TEMPLATE,
)
from generator.text_generator import generate_visual_theme

load_dotenv()


def generate_image(quote_data: Mapping[str, str]) -> str:
    """Generate an image for a quote and save it to disk.

    Args:
        quote_data: Dictionary containing quote text ('q') and author ('a').

    Returns:
        Path to the generated image file.
    """
    # Step 1: Generate quote-relevant visual theme
    visual_theme = generate_visual_theme(quote_data)
    if visual_theme is None:
        raise RuntimeError("Failed to generate visual theme")

    # Step 2: Initialize Hugging Face Inference client
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN environment variable is missing")

    client = InferenceClient(IMAGE_GENERATION_MODEL, token=hf_token)

    # Step 3: Read prompt template
    with open(PROMPT_IMAGE_GENERATION_TEMPLATE, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(visual_theme=visual_theme)

    logging.info("Generating FLUX background with theme: %s", visual_theme)
    image = client.text_to_image(prompt=prompt)

    image.save(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)
    logging.info("Background saved: %s", OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT)

    return OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT
