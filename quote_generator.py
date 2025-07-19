# 1. Load quote for today
import json
import requests

from const import FILE_QUOTE_TODAY


def get_todays_quote():
    response = requests.get("https://zenquotes.io/api/today")
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and data:
        with open(FILE_QUOTE_TODAY, "w") as f:
            json.dump(data[0], f, indent=4)
        return data[0]
    else:
        raise ValueError("Failed to fetch quote from API.")


def main():
    quote = get_todays_quote()
    print(f"Today's quote: {quote}")
    return quote


if __name__ == "__main__":
    main()
