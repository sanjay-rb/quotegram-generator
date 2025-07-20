# Quotegram Generator

An automated, AI-powered pipeline that generates quote-based visual content — including stylized images, hashtags, videos, and Telegram messages. It runs automatically via GitHub Actions on a schedule or when new changes are pushed to the main branch.

---

## ✨ Features

* Fetches daily quotes from [ZenQuotes API](https://zenquotes.io/api/today)
* Generates stylized images using Hugging Face's `FLUX.1-schnell` model
* Creates relevant hashtags using OpenRouter’s `moonshotai/kimi-k2:free` model
* Builds engaging short videos using MoviePy
* Sends the generated video directly to a Telegram chat or channel
* Fully automated with GitHub Actions

---

## 🛠️ Project Structure

The project includes modular Python scripts organized under a `generator/` directory:

* Quote fetching
* Image generation
* Hashtag creation
* Video assembly
* Telegram message generation and delivery

---

## 🚀 How It Works

This project automates the content creation process end-to-end:

1. Fetches a motivational quote using ZenQuotes API.
2. Converts the quote into an AI-generated image using Hugging Face’s `FLUX.1-schnell`.
3. Generates relevant hashtags using OpenRouter’s Kimi-K2 model.
4. Assembles a short video using MoviePy (image and text composition).
5. Uploads the final video to Telegram using the Telegram Bot API.
6. All steps run via GitHub Actions, on a schedule or push.

---

## 🔁 Automation Schedule & Usage Limits

The workflow runs automatically:

* On every push to the `main` branch
* On a fixed schedule: every **Monday, Wednesday, and Friday at 10:00 AM IST**

> ⚠️ **Note:** The schedule is set to thrice weekly to stay within the Hugging Face Inference API monthly usage limit of approximately \$0.10. Running more frequently may exceed your free tier or budget.

---

## 🔐 Environment Variables

The following environment variables are required and should be stored in a base64-encoded `.env` file uploaded to GitHub Secrets as `DOTENV`:

* `HF_TOKEN` – Hugging Face API Key
* `OPEN_ROUTER_API_KEY` – OpenRouter API Key
* `TELEGRAM_BOT_TOKEN` – Telegram Bot Token
* `TELEGRAM_CHAT_ID` – Target Telegram chat or channel ID

---

## 📦 Requirements

Core dependencies include:

* `python-dotenv` (for local development)
* `requests`
* `moviepy` (requires FFmpeg)
* OpenAI / OpenRouter Client
* Hugging Face Inference Client


These are defined in `requirements.txt`.

---

## 🔗 APIs & Services Used

| Purpose            | Provider      | Model / API                            |
| ------------------ | ------------- | -------------------------------------- |
| Quote Fetching     | ZenQuotes     | Daily Quote API                        |
| Image Generation   | Hugging Face  | `black-forest-labs/FLUX.1-schnell`     |
| Hashtag Generation | OpenRouter AI | `moonshotai/kimi-k2:free`              |
| Video Creation     | MoviePy       | Local Python-based generation (FFmpeg) |
| Telegram Delivery  | Telegram API  | `sendVideo` endpoint                   |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤖 Built for Automation

Perfect for creators, content bots, or marketing workflows that benefit from regular, high-quality quote-based video content shared directly to Telegram — with zero manual intervention.

---
