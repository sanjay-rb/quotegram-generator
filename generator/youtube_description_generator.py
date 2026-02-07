import json
import os
import re
import traceback
from openai import OpenAI
from dotenv import load_dotenv


def generate_youtube_description(quote_data: dict) -> list:
    try:
        load_dotenv()
        OUT_YOUTUBE_DESCRIPTION_TODAY_FILE = os.getenv(
            "OUT_YOUTUBE_DESCRIPTION_TODAY_FILE"
        )

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPEN_ROUTER_API_KEY"],
        )

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating YouTube description: {quote} - {author}")

        prompt = (
            f"Generate a YouTube video description for a short based on the quote:\n\n{quote} - {author}\n\n"
            ". Include a concise opening hook, a short description of the quote/context, a call-to-action (subscribe, like, comment), and at least 10 relevant hashtags. "
            "Make the final output easy to copy-paste by surrounding it between --- markers."
        )

        completion = client.chat.completions.create(
            extra_body={"reasoning": {"enabled": True}},
            model="openrouter/free",
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

        with open(OUT_YOUTUBE_DESCRIPTION_TODAY_FILE, "w") as f:
            f.write(content.strip())

        return content.strip()
    except Exception as e:
        print(f"Error generating youtube description: {e}")
        traceback.print_exc()
        return None


def main():
    load_dotenv()
    OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    output = generate_youtube_description(quote_data)
    if output:
        print("Generated YouTube Description:", output)
    else:
        raise RuntimeError("Failed to generate youtube description.")


if __name__ == "__main__":
    main()
