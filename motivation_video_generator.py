from moviepy import (
    CompositeAudioClip,
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    vfx,
)
from dotenv import load_dotenv

from const import FILE_BACKGROUND_VIDEO, FILE_MOTIVATION_TODAY, FILE_QUOTE_TODAY
from quote_generator import get_todays_quote

# Load environment variables
load_dotenv()


# 3. Create video with text and voiceover
def create_motivational_video(quote):

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
        text=f"{quote.get("q", "Bitterness is like a cancer that enters the soul.")}\n- {quote.get("a", "Sir Terry Waite")}",
        font="Arial.ttf",
        font_size=70,
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


# 4. Main pipeline
def main():
    with open(FILE_QUOTE_TODAY, "r") as f:
        quote = dict(f.read())
    print(f"Today's quote: {quote}")
    create_motivational_video(quote)


if __name__ == "__main__":
    main()
