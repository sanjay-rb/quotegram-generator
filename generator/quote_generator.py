"""
Generate quotes for the Quotegram application.

This module retrieves a daily quote from the ZenQuotes API and provides
a fallback quote if the external request fails.
"""

import logging
from typing import Dict

import requests


def generate_quote() -> Dict[str, str]:
    """Fetch the daily quote from zenquotes.io.

    Returns:
        A dictionary containing the quote text, author, and HTML markup.
        Falls back to a static quote if the request fails.
    """
    try:
        logging.info("Generating quote from zenquotes.io")
        response = requests.get(
            "https://zenquotes.io/api/today",
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        return data[0]

    except requests.RequestException as exc:
        logging.error(
            "Error occurred while generating quote from zenquotes.io: %s",
            exc,
        )
        logging.info("Generating fallback quote")

        return {
            "q": "Create each day anew.",
            "a": "Morihei Ueshiba",
            "h": (
                "<blockquote>&ldquo;Create each day anew.&rdquo; "
                "&mdash; <footer>Morihei Ueshiba</footer></blockquote>"
            ),
        }
