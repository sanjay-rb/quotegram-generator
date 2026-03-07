"""
common/functions.py

This module provides utility functions for interacting with the OpenRouter AI API,
including sending prompts and retrieving generated text.
"""

import logging
import os
import re
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

from common.constants import TEXT_GENERATION_MODEL


def ask_open_router(prompt: str) -> Optional[str]:
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

    content = completion.choices[0].message.content
    if content is None:
        logging.error("No content in AI response.")
        return None

    # Extract content between --- markers
    output = content.strip()
    match = re.search(r"---\s*(.*?)\s*---", output, re.DOTALL)

    if match:
        return match.group(1).strip()

    logging.warning("No content found between --- markers.")
    return output.strip()


def ask_llm_for_fix(error: str, traceback: str) -> Optional[str]:
    """
    Ask the LLM for a fix suggestion given an error and traceback.

    Args:
        error: The error message.
        traceback: The full traceback string.

    Returns:
        The suggested fix, or None if failed.
    """
    prompt = f"""
I encountered the following error in my Python code:

Error: {error}

Traceback:
{traceback}

Please suggest a fix for this issue. Provide a concise explanation and the corrected code if applicable.
"""
    return ask_open_router(prompt)
