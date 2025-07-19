import json
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import re
from const import FILE_HASHTAG_TODAY, FILE_QUOTE_TODAY

load_dotenv()

client = InferenceClient(
    provider="novita",
    api_key=os.environ["HF_TOKEN"],
)


def generate_innovative_hashtags(quote: str) -> list:
    prompt = (
        f"Generate a creative, innovative, and contextually relevant list of hashtags for a "
        f'inspirational video featuring this quote:\n\n"{quote}"\n\n'
        f"Provide only hashtags starting with #, separated by spaces or commas. No generic tags like "
        f"#Facebook or #Twitter. Make hashtags catchy, unique, and suitable for TikTok, Instagram, and YouTube Shorts."
    )

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct",
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract hashtags - words starting with #
    hashtags = re.findall(r"#\w+", str(completion))

    # Deduplicate while preserving order
    seen = set()
    unique_hashtags = []
    for tag in hashtags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_hashtags.append(tag)

    with open(FILE_HASHTAG_TODAY, "w") as f:
        f.write(" ".join(unique_hashtags))
    print(f"Hashtags saved to {FILE_HASHTAG_TODAY}")

    return unique_hashtags


def main():
    with open(FILE_QUOTE_TODAY, "r") as f:
        quote_data = json.load(f)

    quote = quote_data.get("q", "Bitterness is like a cancer that enters the soul.")
    tags = generate_innovative_hashtags(quote)
    print("Generated Hashtags:", tags)


# Example usage
if __name__ == "__main__":
    main()
