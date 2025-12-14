"""Telegram bot for Xyber Documentation RAG."""

import asyncio

from telegram import Update
from telegram import error as tg_error
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.config import settings
from src.core.rag import RAGPipeline
from src.ingestion.store import DocumentStore
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Telegram message limits
MAX_MESSAGE_LENGTH = 4096
TYPING_TIMEOUT = 30


class XyberTelegramBot:
    """Telegram bot for Xyber documentation queries."""

    def __init__(self):
        """Initialize the Telegram bot."""
        self.document_store = DocumentStore()
        self.rag_pipeline = RAGPipeline(self.document_store)
        self.application = None
        logger.info("XyberTelegramBot initialized")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        welcome_text = (
            "🚀 Welcome to the Xyber Documentation Chatbot!\n\n"
            "Ask any question about Xyber documentation."
        )
        await update.message.reply_text(welcome_text)

    async def handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle incoming messages."""
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        question = update.message.text.strip()

        if not question:
            return
        # Process query through RAG pipeline
        try:
            # Process query through RAG pipeline
            result = await asyncio.wait_for(
                self.rag_pipeline.query(question), timeout=TYPING_TIMEOUT
            )

            # Build response message
            response_text = result["answer"]

            # Add sources if available
            if result.get("sources"):
                response_text += "\n\n📚 Sources:"
                for source in result["sources"][:3]:  # Limit to 3 sources
                    response_text += f"\n• {source}"

            # Add stats
            response_text += (
                f"\n\n✅ Found {result.get('retrieved_chunks', 0)} relevant chunks"
            )

            # Split message if too long
            if len(response_text) > MAX_MESSAGE_LENGTH:
                # Send in parts
                for i in range(0, len(response_text), MAX_MESSAGE_LENGTH):
                    chunk = response_text[i : i + MAX_MESSAGE_LENGTH]
                    await update.message.reply_text(chunk, parse_mode="HTML")
            else:
                await update.message.reply_text(response_text, parse_mode="HTML")

            logger.info(f"Response sent to {user_name}")

        except asyncio.TimeoutError:
            logger.warning(f"Query timeout for user {user_name}")
            await update.message.reply_text(
                "⏱️ The query took too long to process. Please try a simpler question."
            )
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await update.message.reply_text(
                f"❌ Error processing your question: {str(e)}\n\nPlease try again or check your question."
            )

    async def error_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.message:
            await update.message.reply_text("❌ An error occurred. Please try again.")

    def setup_handlers(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def run(self) -> None:
        """Run the Telegram bot."""
        self.application = (
            Application.builder().token(settings.telegram_bot_token).build()
        )

        self.setup_handlers()


async def run_telegram_bot():
    """Run the Telegram bot."""
    bot = XyberTelegramBot()
    await bot.run()


def run_telegram_bot_sync():
    """Run the Telegram bot synchronously."""
    # Use the blocking run_polling() runner so the process stays alive
    # and handlers (e.g. /start) continue to receive updates.
    application = Application.builder().token(settings.telegram_bot_token).build()
    bot = XyberTelegramBot()
    # Attach the application and register handlers
    bot.application = application
    bot.setup_handlers()

    logger.info("Starting Telegram bot (blocking run_polling)...")
