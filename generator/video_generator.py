import logging
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
import random


from common.constants import (
    OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
    RES_BACKGROUND_IMAGE,
    RES_BGMS,
    RES_FONT_FILE,
    SAFE_PADDING,
    VIDEO_FPS,
    VIDEO_LENGTH,
    VIDEO_SIZE,
)


# 3. Create video with text and voiceover
def generate_video(quote_data, image_path) -> str:
    # Load environment variables
    load_dotenv()

    quote = quote_data.get("q")
    author = quote_data.get("a")
    logging.info(f"Generating quotegram video: {quote} - {author}")

    # Load background image (fallback logic)
    if os.path.exists(image_path):
        clip = ImageClip(image_path, duration=VIDEO_LENGTH).resized(new_size=VIDEO_SIZE)
    else:
        clip = ImageClip(RES_BACKGROUND_IMAGE, duration=VIDEO_LENGTH).resized(
            new_size=VIDEO_SIZE
        )

    # Semi-transparent overlay
    overlay = ColorClip(
        size=VIDEO_SIZE, color=(0, 0, 0, int(255 * 0.5)), duration=VIDEO_LENGTH
    )
    overlay = overlay.with_effects([vfx.CrossFadeIn(duration=5)])

    # --- TEXT WRAPPING ---
    import textwrap

    text_width = VIDEO_SIZE[0] - 2 * SAFE_PADDING["left_right"]
    text_height = VIDEO_SIZE[1] - SAFE_PADDING["top"] - SAFE_PADDING["bottom"]

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
            duration=VIDEO_LENGTH,
            transparent=True,
        )
        .with_position(("center", SAFE_PADDING["top"]))
        .with_effects([vfx.CrossFadeIn(duration=5)])
    )

    # --- ADD BGM (Background Music) ---
    RES_BGM_FILE = random.choice(RES_BGMS)
    if os.path.exists(RES_BGM_FILE):
        logging.info("Adding background music: %s", RES_BGM_FILE)

        bgm = AudioFileClip(RES_BGM_FILE)

        # Loop background music if it's shorter than the video
        if bgm.duration < VIDEO_LENGTH:
            loop_count = int(VIDEO_LENGTH // bgm.duration) + 1
            bgm = bgm.loop(n=loop_count)

        # Trim the BGM to exactly match the video length
        bgm = bgm.with_duration(VIDEO_LENGTH)

        # MoviePy 2.x requires CompositeAudioClip
        audio = CompositeAudioClip([bgm]).with_duration(VIDEO_LENGTH)

    else:
        logging.warning("⚠ No BGM file found at: %s", RES_BGM_FILE)
        audio = None

    # --- FINAL VIDEO ---
    final_video = CompositeVideoClip([clip, overlay, txt_clip])

    # Attach audio
    if audio:
        final_video = final_video.with_audio(audio)
        logging.info("Background music added to the video.")
    final_video.write_videofile(
        OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
        fps=VIDEO_FPS,
        audio_codec="aac",
    )

    return OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT
