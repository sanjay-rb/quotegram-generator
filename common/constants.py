"""
This module defines constants used across the QuoteGram Generator project.
"""

# CONSTANTS
SAFE_PADDING = {
    "left_right": 150,  # Horizontal padding
    "top": 250,
    "bottom": 350,
}

VIDEO_SIZE = 1080, 1920
VIDEO_LENGTH = 10  # seconds
VIDEO_FPS = 30

# MODELS
IMAGE_GENERATION_MODEL = "black-forest-labs/FLUX.1-dev"
TEXT_GENERATION_MODEL = "openrouter/free"

# PROMPT TEMPLATES
PROMPT_TITLE_TEMPLATE = "prompts/title_prompt.txt"
PROMPT_DESCRIPTION_TEMPLATE = "prompts/description_prompt.txt"
PROMPT_VISUAL_THEME_TEMPLATE = "prompts/visual_theme_prompt.txt"
PROMPT_IMAGE_GENERATION_TEMPLATE = "prompts/image_generation_prompt.txt"

# RESOURCE FILES
RES_FONT_FILE = "resource/My-WinkyRough.ttf"
RES_BACKGROUND_IMAGE = "resource/background_image.png"
RES_BGMS = [
    "resource/background_music_1.mp3",
    "resource/background_music_2.mp3",
    "resource/background_music_3.mp3",
    "resource/background_music_4.mp3",
    "resource/background_music_5.mp3",
    "resource/background_music_6.mp3",
    "resource/background_music_7.mp3",
]

# OUTPUT FILES
OUT_QUOTE_TODAY_FILE = "output/quote_today.json"
OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT = "output/quotegram_video.mp4"
OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT = "output/quotegram_image.jpg"
OUT_YOUTUBE_TITLE_TODAY_FILE = "output/youtube_title_today.txt"
OUT_INSTA_CAPTION_TODAY_FILE = "output/insta_caption_today.txt"
OUT_YOUTUBE_URL_TODAY_FILE = "output/youtube_url_today.txt"
OUT_INSTA_URL_TODAY_FILE = "output/insta_url_today.txt"
