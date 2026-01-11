import json
import os
import re
import traceback
from openai import OpenAI
from dotenv import load_dotenv


def generate_insta_caption(quote_data: dict) -> list:
    try:
        load_dotenv()
        OUT_INSTA_CAPTION_TODAY_FILE = os.getenv("OUT_INSTA_CAPTION_TODAY_FILE")

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPEN_ROUTER_API_KEY"],
        )

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))

        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating hashtags: {quote} - {author}")

        prompt = f"Generate a instagram reels caption with atleast 25 hashtags for the quote: \n\n{quote} - {author}\n\n. Make it fesible to copy paste directly between --- markers."

        completion = client.chat.completions.create(
            extra_body={},
            model="arcee-ai/trinity-mini:free",
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

        with open(OUT_INSTA_CAPTION_TODAY_FILE, "w") as f:
            f.write(content.strip())

        return content.strip()
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        traceback.print_exc()
        return None


def main():
    load_dotenv()
    OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    output = generate_insta_caption(quote_data)
    if output:
        print("Generated Instagram Caption:", output)
    else:
        raise RuntimeError("Failed to generate hashtags.")


if __name__ == "__main__":
    main()
