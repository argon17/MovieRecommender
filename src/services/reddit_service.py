import logging
import praw

class RedditService:
    """Handles all interactions with the Reddit API."""
    def __init__(self, client_id, client_secret, user_agent):
        if not all([client_id, client_secret, user_agent]):
            raise ValueError("Reddit API credentials are not fully configured.")
        
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )
        logging.info("RedditService initialized successfully.")

    def get_comments(self, subreddits, limit_per_subreddit=100):
        """
        Fetches the most recent comments from a list of subreddits.
        """
        logging.info(f"Attempting to fetch comments from subreddits: {subreddits}")
        all_comments = []
        try:
            for sub_name in subreddits:
                logging.info(f"Fetching comments from r/{sub_name}...")
                subreddit = self.reddit.subreddit(sub_name)
                # Fetch comments from 'hot' posts for relevance
                for submission in subreddit.hot(limit=10):
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list()[:limit_per_subreddit // 10]:
                        if comment.body and len(comment.body) > 50:
                            all_comments.append(comment.body)
            
            logging.info(f"Successfully fetched {len(all_comments)} comments.")
            return "\n---\n".join(all_comments)

        except Exception as e:
            logging.error(f"Failed to fetch comments from Reddit: {e}")
            return None