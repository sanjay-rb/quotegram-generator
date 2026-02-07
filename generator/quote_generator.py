import requests
import logging


def generate_quote() -> dict:
    try:
        logging.info(f"Generating quote from zenquotes.io")
        response = requests.get("https://zenquotes.io/api/today")
        response.raise_for_status()
        data = response.json()
        return data[0]
    except Exception as e:
        logging.error(f"Unexpected error occurred while generating quote: {e}")
        logging.error(f"Generating fallback quote")
        return {
            "q": "Create each day anew.",
            "a": "Morihei Ueshiba",
            "h": "<blockquote>&ldquo;Create each day anew.&rdquo; &mdash; <footer>Morihei Ueshiba</footer></blockquote>",
        }
