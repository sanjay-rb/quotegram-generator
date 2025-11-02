import json
import os
import re
import traceback
from openai import OpenAI
from dotenv import load_dotenv

from const import *


def generate_youtube_title(quote_data: dict) -> list:
    try:
        load_dotenv()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPEN_ROUTER_API_KEY"],
        )

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating hashtags: {quote} - {author}")

        prompt = f"Generate a youtube video title for the quote: \n\n{quote} - {author}\n\n within 100 characters. Make it fesible to copy paste directly between --- markers."

        completion = client.chat.completions.create(
            extra_body={},
            model="nvidia/nemotron-nano-9b-v2:free",
            messages=[{"role": "user", "content": prompt}],
        )
        output = completion.choices[0].message.content.strip()

        # Extract content between --- markers
        match = re.search(r"---\s*(.*?)\s*---", output, re.DOTALL)

        if match:
            content = match.group(1).strip()
        else:
            print("No content found between --- markers.")
            content = completion.choices[0].message.content.strip()

        with open(OUT_YOUTUBE_TITLE_TODAY_FILE, "w") as f:
            f.write(content.strip())

        return content.strip()

    except Exception as e:
        print(f"Error generating hashtags: {e}")
        traceback.print_exc()
        return None


def main():
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    output = generate_youtube_title(quote_data)
    if output:
        print("Generated Youtube Title:", output)
    else:
        raise RuntimeError("Failed to generate hashtags.")


if __name__ == "__main__":
    main()
