from moviepy import (
    CompositeAudioClip,
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    vfx,
)
import requests

# Paths
BACKGROUND_VIDEO = "background.mp4"  # Use a royalty-free video or your own
OUTPUT_VIDEO = "motivation_today.mp4"


# 1. Load quote for today
def get_today_quote():
    response = requests.get("https://zenquotes.io/api/today")
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list) and data:
        return data[0]
    else:
        raise ValueError("Failed to fetch quote from API.")


# 3. Create video with text and voiceover
def create_motivational_video(quote, background_path, output_path):
    # Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
    # Reduce the audio volume to 80% of its original volume

    clip = (
        VideoFileClip(background_path)
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
    final_video.write_videofile(output_path)


# 4. Main pipeline
def main():
    quote = get_today_quote()
    print(f"Today's quote: {quote}")
    create_motivational_video(quote, BACKGROUND_VIDEO, OUTPUT_VIDEO)


if __name__ == "__main__":
    main()
