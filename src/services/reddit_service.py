import logging
from typing import List, Optional
import asyncpraw
from asyncpraw.exceptions import AsyncPRAWException

class RedditService:
    """Handles all interactions with the Reddit API."""
    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        """
        Initialize the Reddit service with API credentials.

        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: Reddit API user agent string
        
        Raises:
            ValueError: If any of the required credentials are missing
        """
        if not all([client_id, client_secret, user_agent]):
            raise ValueError("Reddit API credentials are not fully configured.")
        
        self.reddit = asyncpraw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        logging.info("RedditService initialized successfully.")

    async def get_comments(self, subreddits: List[str], limit_per_subreddit: int = 100) -> Optional[str]:
        """
        Fetches the most recent comments from a list of subreddits.

        Args:
            subreddits: List of subreddit names to fetch comments from
            limit_per_subreddit: Maximum number of comments to fetch per subreddit

        Returns:
            A string containing all comments joined with separators, or None if an error occurs
        """
        logging.info("Attempting to fetch comments from subreddits: %s", subreddits)
        all_comments = []
        try:
            for sub_name in subreddits:
                logging.info("Fetching comments from r/%s...", sub_name)
                subreddit = await self.reddit.subreddit(sub_name)
                # Fetch comments from 'hot' posts for relevance
                async for submission in subreddit.hot(limit=10):
                    submission.comments.replace_more(limit=0)
                    async for comment in submission.comments.list()[:limit_per_subreddit // 10]:
                        if comment.body and len(comment.body) > 50:
                            all_comments.append(comment.body)
            
            logging.info("Successfully fetched %d comments.", len(all_comments))
            return "\n---\n".join(all_comments)

        except AsyncPRAWException as e:
            logging.error("Failed to fetch comments from Reddit: %s", e)
            return None
