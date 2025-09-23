import logging
from typing import Union
import telegram
from telegram.error import TelegramError

class TelegramService:
    """Handles sending messages via the Telegram Bot API."""
    def __init__(self, bot_token: str, chat_id: Union[str, int]) -> None:
        """
        Initialize the Telegram service.

        Args:
            bot_token: Telegram Bot API token
            chat_id: Telegram chat ID to send messages to

        Raises:
            ValueError: If bot_token or chat_id is missing
        """
        if not all([bot_token, chat_id]):
            raise ValueError("Telegram Bot Token or Chat ID is not configured.")
        
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
        logging.info("TelegramService initialized successfully.")

    async def send_message(self, message: str) -> bool:
        """
        Sends a Markdown-formatted message to the configured chat.

        Args:
            message: The message to send (Markdown formatted)

        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        logging.info("Attempting to send message to Telegram...")
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logging.info("Message sent successfully to Telegram.")
            return True
        except TelegramError as e:
            logging.error("Failed to send message to Telegram: %s", e)
            return False
