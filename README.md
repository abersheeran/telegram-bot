# Telegram Bot

A Telegram bot that uses AI to generate content.

## Setup

Write the following in `.env` file:

```.env
TG_BOT_TOKEN=<your bot token>

GEMINI_PRO_KEY=<your gemini pro key>
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
