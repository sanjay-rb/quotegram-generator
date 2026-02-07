"""
common/functions.py

This module provides utility functions for interacting with the OpenRouter AI API,
including sending prompts and retrieving generated text.
"""

import logging
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from common.constants import TEXT_GENERATION_MODEL


def ask_open_router(prompt: str) -> str:
    """
    Sends a prompt to the OpenRouter AI API and retrieves the generated response.

    The function expects the response to optionally include content
    between '---' markers. If such content exists, only that portion
    is returned; otherwise, the full response is returned.

    Args:
        prompt (str): The prompt string to send to the AI model.

    Returns:
        str: The extracted content from the AI response, or the full response
        if no markers are found.
    """
    load_dotenv()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPEN_ROUTER_API_KEY"],
    )

    completion = client.chat.completions.create(
        extra_body={"reasoning": {"enabled": True}},
        model=TEXT_GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract content between --- markers
    output = completion.choices[0].message.content.strip()
    match = re.search(r"---\s*(.*?)\s*---", output, re.DOTALL)

    if match:
        return match.group(1).strip()

    logging.warning("No content found between --- markers.")
    return output.strip()
