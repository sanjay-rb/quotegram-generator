# Quotegram Generator

An automated Python toolkit that generates quote-based visual content (images and short videos) and uploads to YouTube. The project is modular — each step can be run independently or wired together in automation (e.g., GitHub Actions).

**Quick highlights:**
- **Fetches** daily quotes from ZenQuotes.
- **Generates** stylized images via Hugging Face Inference.
- **Creates** short videos (MoviePy + FFmpeg).
- **Uploads** to YouTube via Google APIs.

**Repo layout (important files)**
- `generator/` : core generators (quote, image, video, captions)
- `upload/` : upload helpers (`youtube_short_upload.py`)
- `requirements.txt` : Python dependencies
- `output/` : default output files produced by scripts

**Minimum Python:** `3.8+`

**Install dependencies**
Run in your venv or system Python:

```bash
python3 -m pip install -r requirements.txt
```

Note: `moviepy` requires `ffmpeg` installed on your system. On macOS you can install with Homebrew:

```bash
brew install ffmpeg
```

**Environment & configuration**
This project reads many values from environment variables (via `python-dotenv`). Provide them using a `.env` file or GitHub Secrets when running in CI. Key variables used across scripts include:

- `HF_TOKEN`: Hugging Face Inference API token
- `OPEN_ROUTER_API_KEY`: OpenRouter API key (for hashtag/caption generation)
- `TELEGRAM_BOT_TOKEN`: Telegram Bot token
- `TELEGRAM_CHAT_ID`: Target chat or channel ID for Telegram uploads
- `OUT_QUOTE_TODAY_FILE`: path written by `generator/quote_generator.py` (default in `output/`)
- `OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT`: image output path used by image generator
- `OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT`: video output path used by the video generator
- `OUT_YOUTUBE_TITLE_TODAY_FILE`: YouTube title for uploads
- `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`: YouTube API credentials

Inspect scripts in `generator/` to find any other env vars your workflow requires.

Usage examples
- Generate today's quote JSON:

```bash
python3 generator/quote_generator.py
```

- Generate an image from the last saved quote:

```bash
python3 generator/image_generator.py
```

- Assemble a video (uses output image + quote text — `generator/quotegram_video_generator.py`):

```bash
python3 generator/quotegram_video_generator.py
```

- Upload a video to YouTube (uses Google OAuth credentials):

```bash
python3 upload/youtube_short_upload.py
```

Running in CI / GitHub Actions
- The repository includes GitHub Actions automation for scheduled runs and manual triggers. Store YouTube API credentials and other secrets in repository secrets and inject them into workflow runs.

Dependencies
- See `requirements.txt` for exact pinned packages used in the project.

Troubleshooting
- If image generation fails, ensure `HF_TOKEN` is valid and not rate-limited.
- If MoviePy fails, verify `ffmpeg` is installed and available on `PATH`.
- For Instagram upload issues, check that `insta_settings.json` contains a valid session and that the `instagrapi` version is compatible.

Contributing
- Fork, create a topic branch, and open a pull request. Keep changes focused and include tests where appropriate.

License
- This project is licensed under the MIT License — see `LICENSE`.

If you'd like, I can:
- run a smoke-check by executing the generators locally (requires credentials),
- or update a GitHub Actions workflow to match this README's quickstart.

