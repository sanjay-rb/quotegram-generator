"""
Generate text prompts for Quotegram content.

This module generates titles, descriptions, and visual themes for quotes
using prompt templates and the OpenRouter API.
"""

import logging
from typing import Dict

from dotenv import load_dotenv

from common.constants import (
    PROMPT_DESCRIPTION_TEMPLATE,
    PROMPT_TITLE_TEMPLATE,
    PROMPT_VISUAL_THEME_TEMPLATE,
)
from common.functions import ask_open_router


load_dotenv()


def _generate_from_template(
    template_path: str,
    quote_data: Dict[str, str],
    log_label: str,
) -> str:
    """Generate text using a prompt template and quote data."""
    quote = quote_data.get("q")
    author = quote_data.get("a")

    logging.info(
        "Generating %s for quote '%s' - %s",
        log_label,
        quote,
        author,
    )

    with open(template_path, "r", encoding="utf-8") as file_handle:
        prompt_template = file_handle.read()

    prompt = prompt_template.format(quote=quote, author=author)
    return ask_open_router(prompt)


def generate_title(quote_data: Dict[str, str]) -> str:
    """Generate a YouTube title for a quote."""
    return _generate_from_template(
        PROMPT_TITLE_TEMPLATE,
        quote_data,
        "title",
    )


def generate_description(quote_data: Dict[str, str]) -> str:
    """Generate a YouTube description for a quote."""
    return _generate_from_template(
        PROMPT_DESCRIPTION_TEMPLATE,
        quote_data,
        "description",
    )


def generate_visual_theme(quote_data: Dict[str, str]) -> str:
    """Generate a visual theme for a quote."""
    return _generate_from_template(
        PROMPT_VISUAL_THEME_TEMPLATE,
        quote_data,
        "visual theme",
    )
