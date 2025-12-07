# CHANGELOG

All notable changes to this project will be documented in this file.

## [1.0.7] - 2025-12-07

### ✨ Features:
- Added Hugging Face Inference integration for image generation using multiple models (including `stabilityai/stable-diffusion-xl-base-1.0` and `black-forest-labs/FLUX.1` variants). Improved prompt design to produce high-quality, no-text images with reserved safe space for overlaying quotes.
- Added Instagram caption and hashtag generation using OpenRouter (`nvidia/nemotron-nano-9b-v2`) to produce ready-to-copy captions with 25+ hashtags.
- Improved video generation with MoviePy: safe padding, text wrapping, semi-transparent overlay, background music selection/looping/trimming, and automatic `moviepy==2.2.1` installation in the runner.
- Added `refresh_token_generator.py` to handle Google OAuth flows and persist YouTube tokens into `.env` for upload automation.

### 🐛 Fixes & Improvements:
- Robust environment-variable fallbacks for quote and asset paths; default quote fallback used on API failures.
- Better error handling and logging across generators to surface failures instead of silent exits.
- Consolidated model choices for image generation and randomized selection for reliability.

### 🛠️ Notes:
- Update environment variables (`HF_TOKEN`, `OPEN_ROUTER_API_KEY`, BGM/asset paths, and output file paths) before running the pipeline.
- Recommended next steps: commit this changelog, tag the release, and bump any packaging/version files if present.

## [1.0.6] - 2025-08-10

### 🔧 Features:
- Introduced predefined hashtags for posts. 
- Added trending hashtag functionality.
- Modified GitHub Actions workflow in `main-branch-push.yml` to improve CI/CD configuration.
- Updated scheduled GitHub Actions cron timing. 
- Reordered steps in GitHub Actions workflow for improved execution flow. 
- Updated image generation with model="stabilityai/stable-diffusion-xl-base-1.0".


## [1.0.0] - 2025-07-21
### 🚀 Initial Release: Quotegram Generator

An AI-powered, fully automated content pipeline that turns motivational quotes into stylized videos and posts them directly.

### 🔧 Features:
- ✅ Fetches daily quotes from ZenQuotes
- 🎨 Generates AI-stylized quote images
- 🏷️ Creates hashtags with a large language model (LLM)
- 🎞️ Builds short videos with MoviePy
- 📲 Sends content to Telegram — all on autopilot
- 🛠️ Powered by GitHub Actions (runs Mon/Wed/Fri at 9 AM IST)