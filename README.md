# Telegram Bot

A Telegram bot that uses AI to generate content.

## Setup

Write the following in `.env` file:

```.env
TG_BOT_TOKEN=<your bot token>

GEMINI_PRO_KEY=<your gemini pro key>

# Optional, if you need to use a reverse proxy
GEMINI_PRO_URL=https://gemini.proxy/v1beta/models/gemini-pro:generateContent
GEMINI_PRO_VISION_URL=https://gemini.proxy/v1beta/models/gemini-pro-vision:generateContent
```

## Usage

```bash
docker compose up --build -d
```

Or, if you want to run it without Docker:

```bash
pdm sync
pdm run python main.py
```
