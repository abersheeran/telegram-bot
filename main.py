import base64
import os

from loguru import logger
from telegram import PhotoSize, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from ai_api import GenerateNetworkError, GenerateResponseError, GenerateSafeError
from ai_api.gemini import (
    initial_gemini_config,
    generate_content,
    Part as GeminiRequestPart,
    Content as GeminiRequestContent,
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message
    assert update.effective_user
    await update.message.reply_text(
        update.message.text or update.message.caption or "?"
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.debug(f"Update: {update}")
    assert update.message
    assert update.effective_user
    parts: list[GeminiRequestPart] = [
        {"text": update.message.text or update.message.caption or ""}
    ]
    photos: dict[str, PhotoSize] = {}
    for photo_size in update.message.photo:
        p = photos.get(photo_size.file_id, photo_size)
        if (p.file_size or 0) <= (photo_size.file_size or 0):
            photos[photo_size.file_id] = photo_size
    for photo_size in photos.values():
        file = await photo_size.get_file()
        image = await file.download_as_bytearray()
        image_base64 = base64.b64encode(image).decode("utf-8")
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_base64}})
    contents: list[GeminiRequestContent] = [{"parts": parts}]
    try:
        response_content = await generate_content(contents)
    except GenerateSafeError as error:
        response_content = "这是不可以谈的话题。"
        logger.warning(f"Safe error: {error}")
    except GenerateResponseError as error:
        response_content = error.message
        logger.exception(f"Response error: {error}")
    except GenerateNetworkError as error:
        response_content = "怎么办？怎么办？派蒙连接不上提瓦特了。"
        logger.warning(f"Network error: {error}")
    else:
        await update.message.reply_markdown_v2(response_content)


async def post_init(app: Application) -> None:
    await initial_gemini_config(
        GEMINI_PRO_KEY, pro_url=GEMINI_PRO_URL, pro_vision_url=GEMINI_PRO_VISION_URL
    )
    logger.info("Gemini client initialized.")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv(verbose=True)

    TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    GEMINI_PRO_KEY = os.environ["GEMINI_PRO_KEY"]
    GEMINI_PRO_URL = os.environ.get("GEMINI_PRO_URL")
    GEMINI_PRO_VISION_URL = os.environ.get("GEMINI_PRO_VISION_URL")

    app = ApplicationBuilder().token(TG_BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(MessageHandler(~filters.COMMAND, ask))
    app.run_polling()
