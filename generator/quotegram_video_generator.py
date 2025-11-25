from datetime import datetime
import json
from moviepy import (
    CompositeAudioClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    vfx,
    ColorClip,
    AudioFileClip,
)
from dotenv import load_dotenv
import os


# 3. Create video with text and voiceover
def generate_quotegram_video(quote_data):
    try:
        SAFE_PADDING = {
            "left_right": 150,  # Horizontal padding
            "top": 250,
            "bottom": 350,
        }

        # Load environment variables
        load_dotenv()

        OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT")
        OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = os.getenv("OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT")
        OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
        RES_BACKGROUND_IMAGE = os.getenv("RES_BACKGROUND_IMAGE")
        RES_FONT_FILE = os.getenv("RES_FONT_FILE")
        RES_BGM_COUNT = os.getenv("RES_BGM_COUNT")

        CONST_DEFAULT_QUOTE = json.loads(os.getenv("CONST_DEFAULT_QUOTE"))
        quote = quote_data.get("q", CONST_DEFAULT_QUOTE["q"])
        author = quote_data.get("a", CONST_DEFAULT_QUOTE["a"])
        print(f"Generating quotegram video: {quote} - {author}")

        # Video config
        size = 1080, 1920
        length = 10  # seconds

        # Load background image (fallback logic)
        if not os.path.exists(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT):
            clip = ImageClip(RES_BACKGROUND_IMAGE, duration=length).resized(
                new_size=size
            )
        else:
            clip = ImageClip(OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT, duration=length).resized(
                new_size=size
            )

        # Semi-transparent overlay
        overlay = ColorClip(size=size, color=(0, 0, 0, int(255 * 0.5)), duration=length)
        overlay = overlay.with_effects([vfx.CrossFadeIn(duration=5)])

        # --- TEXT WRAPPING ---
        import textwrap

        text_width = size[0] - 2 * SAFE_PADDING["left_right"]
        text_height = size[1] - SAFE_PADDING["top"] - SAFE_PADDING["bottom"]

        wrapped_quote = textwrap.fill(quote, width=text_width // 25)

        txt_clip = (
            TextClip(
                text=f"{wrapped_quote}\n- {author}",
                font=RES_FONT_FILE,
                font_size=55,
                color="white",
                size=(text_width, text_height),
                method="caption",
                text_align="center",
                duration=length,
                transparent=True,
            )
            .with_position(("center", SAFE_PADDING["top"]))
            .with_effects([vfx.CrossFadeIn(duration=5)])
        )

        # --- ADD BGM (Background Music) ---
        random_index = datetime.now().microsecond % RES_BGM_COUNT + 1
        RES_BGM_FILE = os.getenv(f"RES_BGM_FILE_{random_index}")
        if os.path.exists(RES_BGM_FILE):
            print("Adding background music:", RES_BGM_FILE)

            bgm = AudioFileClip(RES_BGM_FILE)

            # Loop background music if it's shorter than the video
            if bgm.duration < length:
                loop_count = int(length // bgm.duration) + 1
                bgm = bgm.loop(n=loop_count)

            # Trim the BGM to exactly match the video length
            bgm = bgm.with_duration(length)

            # MoviePy 2.x requires CompositeAudioClip
            audio = CompositeAudioClip([bgm]).with_duration(length)

        else:
            print("⚠ No BGM file found at:", RES_BGM_FILE)
            audio = None

        # --- FINAL VIDEO ---
        final_video = CompositeVideoClip([clip, overlay, txt_clip])

        # Attach audio
        if audio:
            final_video = final_video.with_audio(audio)
            print("Background music added to the video.")
        final_video.write_videofile(
            OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
            fps=24,
            audio_codec="aac",
        )

        return OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT

    except Exception as e:
        print(f"Error generating quotegram video: {e}")
        return None


def main():
    load_dotenv()
    OUT_QUOTE_TODAY_FILE = os.getenv("OUT_QUOTE_TODAY_FILE")
    with open(OUT_QUOTE_TODAY_FILE, "r") as f:
        quote_data = json.load(f)

    video = generate_quotegram_video(quote_data)
    if video:
        print("Generated quotegram video:", video)
    else:
        raise RuntimeError("Failed to generate quotegram video.")


if __name__ == "__main__":
    main()
