import asyncio
import logging
from src.config.settings import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    GEMINI_API_KEY,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    MOVIE_SUBREDDITS,
    LOGGING_CONFIG
)
from src.services.reddit_service import RedditService
from src.services.llm_service import LLMService
from src.services.telegram_service import TelegramService
from src.bot.movie_bot import MovieBot

# Configure logging
logging.basicConfig(**LOGGING_CONFIG)

async def main():
    """Initializes services and runs the bot."""
    try:
        # Initialize Services
        reddit_service = RedditService(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        llm_service = LLMService(api_key=GEMINI_API_KEY)
        telegram_service = TelegramService(
            bot_token=TELEGRAM_BOT_TOKEN,
            chat_id=TELEGRAM_CHAT_ID
        )

        # Initialize and Run the Bot
        bot = MovieBot(reddit_service, llm_service, telegram_service)
        await bot.run_weekly_flow(MOVIE_SUBREDDITS)

    except ValueError as e:
        logging.critical(f"Configuration error: {e}. Please check your .env file.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred in main: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot script manually interrupted.")