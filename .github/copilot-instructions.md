<!-- GitHub Copilot Instructions for the quotegram-generator repo -->

# Purpose
Concise, repo-specific guidance to help an AI coding assistant be productive here.

**Big picture**
- This repo generates "quotegram" social assets and (optionally) uploads them. Main areas:
  - `generator/`: creates quotes, titles, descriptions, images, and videos
  - `upload/`: platform upload helpers (YouTube uploader)
  - `output/`: artifact files produced/consumed by scripts
  - `resource/`: background images, fonts, and BGM assets
- Typical flow: `output/quote_today.json` -> generators read/write `output/*` files -> `upload/` or `generator/telegram_message_generator.py` consumes outputs to post or notify.

**Key files & examples**
- `generator/quote_generator.py`: fetches quote (fallback to built-in JSON if network fails).
- `generator/title_generator.py` and `generator/description_generator.py`: call the OpenRouter/OpenAI-compatible client and write to `OUT_YOUTUBE_TITLE_TODAY_FILE` and `OUT_YOUTUBE_DESCRIPTION_TODAY_FILE` respectively.
- `generator/video_generator.py`: produces `OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT` and uses env keys `RES_BACKGROUND_IMAGE`, `RES_FONT_FILE`, `RES_BGM_COUNT`, `RES_BGM_FILE_{n}`.
- `generator/telegram_message_generator.py`: posts video/title/url to Telegram using `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
- `upload/youtube_short_uploader.py`: uploads `OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT`, sets thumbnail `OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT`, and writes `OUT_YOUTUBE_URL_TODAY_FILE` (requires `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`).

**Important env vars used across the codebase**
- Output file keys: `OUT_QUOTE_TODAY_FILE`, `OUT_YOUTUBE_TITLE_TODAY_FILE`, `OUT_YOUTUBE_DESCRIPTION_TODAY_FILE`, `OUT_YOUTUBE_URL_TODAY_FILE`, `OUT_QUOTEGRAM_VIDEO_FINAL_OUTPUT`, `OUT_QUOTEGRAM_IMAGE_FINAL_OUTPUT`.
- LLM: `OPEN_ROUTER_API_KEY`.
- Defaults/resources: `CONST_DEFAULT_QUOTE` (JSON string), `RES_BACKGROUND_IMAGE`, `RES_FONT_FILE`, `RES_BGM_COUNT`, `RES_BGM_FILE_1...N`.
- Posting/upload creds: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`.

**Conventions & patterns to preserve**
- Environment-driven I/O: scripts expect `.env` values and write/read fixed files. Avoid changing the env keys without updating all consumers.
- LLM outputs are expected to be framed between `---` markers; generators parse with `r"---\s*(.*?)\s*---"` in a DOTALL match. Keep this format when editing prompts.
- Generators return the content (string) or `None` and also write outputs to the file paths defined by environment variables.
- Error handling is intentionally minimal: exceptions are printed and `None` returned; `main()` often raises `RuntimeError` on failure — CI should treat non-zero exits as failures.

**Repo-specific gotchas / things to watch for**
- Some `main()` functions call different function names than those declared (example: `description_generator.py`'s `main()` references `generate_youtube_description` while the defined function is `generate_description`). Check function names when editing or adding runners.
- Tests use `unittest` and relative imports; run them from repo root with `PYTHONPATH=.` to avoid ImportErrors.
- `video_generator.py` installs `moviepy==2.2.1` at runtime to avoid compatibility issues — expect that side-effect when running locally.
- Instagram-related scripts/settings were intentionally removed from the repo; do not reintroduce `insta_*` references unless you also restore their files and settings.

**Integration points**
- OpenRouter/OpenAI-compatible chat completions: `OpenAI(base_url="https://openrouter.ai/api/v1", api_key=...)` and `client.chat.completions.create(..., model="openrouter/free")`.
- YouTube upload: Google OAuth `Credentials` + `googleapiclient`.
- Telegram: direct HTTP calls to Telegram Bot API.

**Run & test commands (concrete)**
- Install deps: `pip install -r requirements.txt`
- Generate a quote JSON: `python generator/quote_generator.py`
- Generate title/description: `python generator/title_generator.py` / `python generator/description_generator.py`
- Build video: `python generator/video_generator.py` (will ensure `moviepy==2.2.1`)
- Upload to YouTube: `python upload/youtube_short_uploader.py`
- Run tests from repo root:
  - `PYTHONPATH=. python -m unittest discover -s test -v`
  - or `PYTHONPATH=. python test/unittest.py`

**When editing code**
- Preserve env-driven contracts; update all consumers if you rename an env key or output filename.
- Update the `---` extraction regex when changing prompt output format.
- Keep generator functions returning content or `None` and writing to env-defined files.

---
If you'd like, I can:
- add a `.env.example` listing the common keys,
- fix the inconsistent `main()` function-name bugs in the generators,
- or add a small `scripts/` runner or `Makefile` to standardize run/test commands. Which should I do next?
