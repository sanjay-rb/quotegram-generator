"""
Generate a Quotegram video with background, text overlay, and background music.

This module creates a video for a quote, including a visual background,
formatted text overlay, optional BGM, and saves it to the final output path.
"""

import logging
import os
import random
import textwrap
from typing import Mapping, Optional

from dotenv import load_dotenv
from moviepy import (
    CompositeAudioClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    vfx,
    ColorClip,
    AudioFileClip,
)


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

load_dotenv()


def generate_video(quote_data: Mapping[str, str], image_path: str) -> str:
    """Generate a Quotegram video and save to disk.

    Args:
        quote_data: Dictionary containing quote text ('q') and author ('a').
        image_path: Path to the background image to use.

    Returns:
        Path to the saved video file.
    """
    quote = quote_data.get("q", "")
    author = quote_data.get("a", "")
    logging.info("Generating quotegram video: '%s' - %s", quote, author)

    # --- Background Image ---
    if os.path.exists(image_path):
        clip = ImageClip(image_path, duration=VIDEO_LENGTH).resized(new_size=VIDEO_SIZE)
    else:
        logging.warning(
            "Background image not found at %s, using default background.", image_path
        )
        clip = ImageClip(RES_BACKGROUND_IMAGE, duration=VIDEO_LENGTH).resized(
            new_size=VIDEO_SIZE
        )

    # --- Semi-transparent overlay ---
    overlay = ColorClip(
        size=VIDEO_SIZE,
        color=(0, 0, 0, int(255 * 0.5)),
        duration=VIDEO_LENGTH,
    ).with_effects([vfx.CrossFadeIn(duration=5)])

    # --- Text Overlay ---
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

    # --- Background Music ---
    audio: Optional[CompositeAudioClip] = None
    if RES_BGMS:
        res_bgm_file = random.choice(RES_BGMS)
        if os.path.exists(res_bgm_file):
            logging.info("Adding background music: %s", res_bgm_file)
            bgm = AudioFileClip(res_bgm_file)

            # Loop BGM if shorter than video
            if bgm.duration < VIDEO_LENGTH:
                loop_count = int(VIDEO_LENGTH // bgm.duration) + 1
                bgm = bgm.loop(n=loop_count)  # pylint: disable=no-member

            # Trim to video length
            bgm = bgm.with_duration(VIDEO_LENGTH)
            audio = CompositeAudioClip([bgm]).with_duration(VIDEO_LENGTH)
        else:
            logging.warning("No BGM file found at: %s", res_bgm_file)
    else:
        logging.warning("RES_BGMS list is empty. No background music added.")

    # --- Compose Final Video ---
    final_video = CompositeVideoClip([clip, overlay, txt_clip])

    if audio:
        final_video = final_video.with_audio(audio)
        logging.info("Background music added to the video.")

    final_video.write_videofile(
        OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT,
        fps=VIDEO_FPS,
        audio_codec="aac",
    )
    logging.info("Quotegram video saved: %s", OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT)

    return OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT
