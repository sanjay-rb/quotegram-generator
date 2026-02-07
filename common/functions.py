import logging
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from common.constants import TEXT_GENERATION_MODEL


def ask_open_router(prompt: str) -> str:
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

    # Extract content between --- markers
    output = completion.choices[0].message.content.strip()
    match = re.search(r"---\s*(.*?)\s*---", output, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        logging.warning("No content found between --- markers.")
        return output.strip()
