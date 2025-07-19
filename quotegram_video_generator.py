import json
from moviepy import (
    CompositeAudioClip,
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    vfx,
)
from dotenv import load_dotenv

from const import (
    DEFAULT_QUOTE,
    FILE_BACKGROUND_VIDEO,
    FILE_FONT,
    FILE_MOTIVATION_TODAY,
    FILE_QUOTE_TODAY,
)

# Load environment variables
load_dotenv()


# 3. Create video with text and voiceover
def generate_quotegram_video(quote_data):
    try:
        quote = quote_data.get("q", DEFAULT_QUOTE["q"])
        author = quote_data.get("a", DEFAULT_QUOTE["a"])
        print(f"Generating quotegram video: {quote} - {author}")

        # Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
        # Reduce the audio volume to 80% of its original volume

        clip = (
            VideoFileClip(FILE_BACKGROUND_VIDEO)
            .subclipped(10, 20)
            .resized(new_size=(1080, 1920))
            .with_volume_scaled(0.8)
        )

        # Generate a text clip. You can customize the font, color, etc.
        txt_clip = TextClip(
            text=f"{quote}\n- {author}",
            font=FILE_FONT,
            font_size=60,
            color="white",
            size=(1080, 1920),
            method="caption",
            text_align="center",
            duration=10,
        ).with_effects([vfx.CrossFadeIn(duration=5)])

        # Overlay the text clip on the first video clip
        final_video = CompositeVideoClip([clip, txt_clip])

        final_video.audio = CompositeAudioClip([AudioFileClip(filename="bgm.mp3")])
        final_video.write_videofile(FILE_MOTIVATION_TODAY)
        return FILE_MOTIVATION_TODAY
    except Exception as e:
        print(f"Error generating quotegram video: {e}")
        return None


def main():
    with open(FILE_QUOTE_TODAY, "r") as f:
        quote_data = json.load(f)

    video = generate_quotegram_video(quote_data)
    if video:
        print("Generated quotegram video:", video)
    else:
        raise RuntimeError("Failed to generate quotegram video.")


if __name__ == "__main__":
    main()
