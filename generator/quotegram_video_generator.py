from datetime import datetime
import json
from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    vfx,
)
from dotenv import load_dotenv
import os

from const import *


# 3. Create video with text and voiceover
def generate_quotegram_video(quote_data):
    try:
        # Load environment variables
        load_dotenv()
        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating quotegram video: {quote} - {author}")

        # Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
        # Resize the video to 1080x1920
        size = 1080, 1920
        # Video Length: 10 seconds
        length = 10

        if not os.path.exists(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT):
            clip = ImageClip(RES_BACKGROUND_IMAGE, duration=length).resized(
                new_size=size
            )
        else:
            clip = ImageClip(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT, duration=length).resized(
                new_size=size
            )

        # Generate a text clip. You can customize the font, color, etc.

        txt_clip = TextClip(
            text=f"{quote}\n- {author}",
            font=RES_FONT_FILE,
            font_size=60,
            color="white",
            bg_color=(0, 0, 0, int(255 * 0.5)),
            size=size,
            method="caption",
            text_align="center",
            duration=length,
            transparent=True,
        ).with_effects([vfx.CrossFadeIn(duration=5)])

        # Overlay the text clip on the first video clip
        final_video = CompositeVideoClip([clip, txt_clip])
        final_video.write_videofile(OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT, fps=24)
        return OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT
    except Exception as e:
        print(f"Error generating quotegram video: {e}")
        return None


def main():
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    video = generate_quotegram_video(quote_data)
    if video:
        print("Generated quotegram video:", video)
    else:
        raise RuntimeError("Failed to generate quotegram video.")


if __name__ == "__main__":
    main()
