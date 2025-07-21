import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

from const import *


def generate_hashtags(quote_data: dict) -> list:
    try:
        load_dotenv()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPEN_ROUTER_API_KEY"],
        )

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating hashtags: {quote} - {author}")

        prompt = (
            f"Generate a creative, innovative, and contextually relevant list of hashtags for a "
            f'inspirational video featuring this quote:\n\n"{quote} - {author}"\n\n'
            f"Provide only hashtags starting with #, separated by spaces or commas. No generic tags like "
            f"#Facebook or #Twitter. Make hashtags catchy, unique, and suitable for TikTok, Instagram, and YouTube Shorts."
        )

        completion = client.chat.completions.create(
            extra_body={},
            model="moonshotai/kimi-k2:free",
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract hashtags - words starting with #
        hashtags = re.findall(r"#\w+", str(completion))

        # TODO: Add predefined hashtags

        # Deduplicate while preserving order
        seen = set()
        unique_hashtags = []
        for tag in hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_hashtags.append(tag)

        with open(OUT_HASHTAGS_TODAY_FILE, "w") as f:
            f.write(" ".join(unique_hashtags))

        return unique_hashtags
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        return None


def main():
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    tags = generate_hashtags(quote_data)
    if tags:
        print("Generated hashtags:", tags)
    else:
        raise RuntimeError("Failed to generate hashtags.")


if __name__ == "__main__":
    main()
