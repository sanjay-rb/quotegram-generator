# CHANGELOG

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-07-27

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