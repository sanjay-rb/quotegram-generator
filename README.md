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

* On a fixed schedule: every **Monday, Wednesday, and Friday at 09:00 AM IST**

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

Here is an updated **README.md** tailored specifically for your code example that uses `InstalledAppFlow` with the YouTube Upload scope and retrieves both access + refresh tokens.

---

# YouTube OAuth Setup (Desktop Client)

This document explains how to create a Google Cloud project, enable the YouTube Data API, generate OAuth 2.0 Desktop Client credentials, and use them in a Python script to obtain **access** and **refresh** tokens.

---

## 📌 Requirements

* Google account
* Python 3.8+
* Installed Python packages:

  ```bash
  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```

---

# 1. Create a Google Cloud Project

1. Go to the Google Cloud Console:
   [https://console.cloud.google.com/](https://console.cloud.google.com/)

2. Click the project dropdown → **New Project**.

3. Enter:

   * **Project Name**
   * **Organization** (optional)
   * **Location**

4. Click **Create**.

---

# 2. Enable the YouTube Data API v3

1. Go to:
   [https://console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)

2. Search **YouTube Data API v3**.

3. Click **Enable**.

---

# 3. Configure OAuth Consent Screen

1. Go to:
   [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)

2. Choose **External** (recommended unless you manage a Google Workspace org).

3. Fill in:

   * **App name** (e.g., `YouTube Upload App`)
   * **User support email**
   * **Developer email**

4. Add no scopes for now (Google will auto-handle YouTube scopes during auth).

5. Save and continue until complete.

---

# 4. Create OAuth 2.0 Client (Desktop App)

1. Go to:
   [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

2. Click **Create Credentials** → **OAuth client ID**.

3. Choose:

   * **Application type:** Desktop app
   * Name: e.g., `YouTube Desktop OAuth`

4. Click **Create**.

5. Download the JSON credentials.
   Save it as:

   ```
   client_secrets.json
   ```

---

# 5. Store Credentials Locally

Place your file in the project directory:

```
your-project/
│
├── client_secrets.json
└── auth.py
```

⚠️ **Never commit client_secrets.json to GitHub.**
Add it to `.gitignore`:

```
client_secrets.json
```

---

# 6. Generate Token

Exec [refresh_token_generator.py](generator/refresh_token_generator.py) which will update your .env file with YOUTUBE_TOKENS.

---

# 7. Notes About Tokens

### ✔ Access Token

* Valid for ~1 hour
* Used for authorized API requests

### ✔ Refresh Token

* Valid long-term
* Used to automatically obtain new access tokens
* Only issued on the **first** consent with “offline access” (default for InstalledAppFlow)

---
