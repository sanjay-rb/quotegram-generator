# 1. Load quote for today
import json
import requests

from const import DEFAULT_QUOTE, FILE_QUOTE_TODAY


def generate_quote():
    try:
        print(f"Generating quote for today...")
        response = requests.get("https://zenquotes.io/api/today")
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data:
            with open(FILE_QUOTE_TODAY, "w") as f:
                json.dump(data[0], f, indent=4)
            return data[0]
        else:
            raise ValueError("Failed to fetch quote from API.")
    except Exception as e:
        print(f"Error generating quote: {e}")
        return DEFAULT_QUOTE


def main():
    quote = generate_quote()
    print(f"Generated quote: {quote}")
    return quote


if __name__ == "__main__":
    main()
