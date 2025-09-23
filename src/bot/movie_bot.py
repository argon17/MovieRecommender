"""Movie recommendation bot orchestrator module."""

import logging
from typing import List
from src.services.reddit_service import RedditService
from src.services.llm_service import LLMService
from src.services.telegram_service import TelegramService

class MovieBot:
    """Orchestrates the workflow of fetching, analyzing, and sending recommendations."""

    def __init__(
        self,
        reddit_service: RedditService,
        llm_service: LLMService,
        telegram_service: TelegramService
    ) -> None:
        """
        Initialize the MovieBot with required services.

        Args:
            reddit_service: Service for fetching Reddit comments
            llm_service: Service for generating recommendations
            telegram_service: Service for sending messages
        """
        self.reddit_service = reddit_service
        self.llm_service = llm_service
        self.telegram_service = telegram_service

    async def run_weekly_flow(self, subreddits: List[str]) -> None:
        """
        Executes the main logic of the bot.

        Args:
            subreddits: List of subreddit names to analyze
        """
        logging.info("Starting the weekly movie recommender bot flow...")

        # 1. Fetch comments from Reddit
        comments_data = await self.reddit_service.get_comments(subreddits)
        if not comments_data:
            logging.error("Could not retrieve comments. Aborting.")
            await self.telegram_service.send_message(
                "Sorry, I couldn't fetch movie data from Reddit this week."
            )
            return

        # 2. Get recommendation from the LLM
        recommendation = self.llm_service.get_movie_recommendation(comments_data)
        if not recommendation:
            logging.error("Could not generate a recommendation. Aborting.")
            await self.telegram_service.send_message(
                "Sorry, I was unable to generate a movie recommendation this week."
            )
            return

        # 3. Send the recommendation to Telegram
        await self.telegram_service.send_message(recommendation)
        logging.info("Bot has finished its weekly run successfully.")
