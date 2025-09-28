"""Main entry point for the Movie Recommender Bot."""

import asyncio
import logging
import sys

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

async def main() -> None:
    """
    Initialize services and run the bot.
    
    This function sets up all required services (Reddit, LLM, Telegram)
    and orchestrates the movie recommendation workflow.
    """
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
        logging.critical("Configuration error: %s. Please check your .env file.", e)
        sys.exit(1)
    except (ConnectionError, TimeoutError, OSError) as e:
        logging.critical("Network or system error occurred: %s", e)
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Bot script interrupted by user.")
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.critical("An unexpected error occurred in main: %s", e)
        sys.exit(1)
    finally:
        logging.info("Shutting down services...")
        await reddit_service.close()
        await telegram_service.close()

def run() -> None:
    """Entry point for the application."""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot script manually interrupted.")
        sys.exit(0)

if __name__ == "__main__":
    run()
