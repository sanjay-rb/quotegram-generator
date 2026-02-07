import logging
from dotenv import load_dotenv

from common.constants import (
    PROMPT_DESCRIPTION_TEMPLATE,
    PROMPT_TITLE_TEMPLATE,
    PROMPT_VISUAL_THEME_TEMPLATE,
)
from common.functions import ask_open_router


def generate_title(quote_data: dict) -> str:
    quote = quote_data.get("q")
    author = quote_data.get("a")
    logging.info(f"Generating title for quote '{quote}' - {author}")

    load_dotenv()
    with open(PROMPT_TITLE_TEMPLATE, "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.format(quote=quote, author=author)

    return ask_open_router(prompt)


def generate_description(quote_data: dict) -> str:
    quote = quote_data.get("q")
    author = quote_data.get("a")
    logging.info(f"Generating description for quote '{quote}' - {author}")

    load_dotenv()
    with open(PROMPT_DESCRIPTION_TEMPLATE, "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.format(quote=quote, author=author)

    return ask_open_router(prompt)


def generate_visual_theme(quote_data: dict) -> str:
    quote = quote_data.get("q")
    author = quote_data.get("a")
    logging.info(f"Generating visual theme for quote '{quote}' - {author}")

    load_dotenv()
    with open(PROMPT_VISUAL_THEME_TEMPLATE, "r") as f:
        prompt_template = f.read()
    prompt = prompt_template.format(quote=quote, author=author)

    return ask_open_router(prompt)
