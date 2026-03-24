import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

from agent.loop import _init_gemini, _chat_gemini, _chat_ollama

load_dotenv()

# Load config from .env
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("TELEGRAM_OWNER_ID"))
BACKEND = os.getenv("LLM_BACKEND", "ollama")       # "gemini" or "ollama"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3")

# If using Gemini, initialize the client once at startup
gemini_client = _init_gemini() if BACKEND == "gemini" else None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Called every time someone sends a text message to the bot."""

    # Security: only respond to you
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized.")
        return

    user_text = update.message.text

    # Call the right backend
    if BACKEND == "gemini":
        result = _chat_gemini(gemini_client, user_text)
    else:
        result = _chat_ollama(OLLAMA_MODEL, user_text)

    await update.message.reply_text(result)


if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()

    # Register the handler: trigger on all text messages that aren't /commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(f"Bot running ({BACKEND}). Send a message on Telegram.")
    app.run_polling()