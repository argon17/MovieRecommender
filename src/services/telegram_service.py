import logging
import telegram

class TelegramService:
    """Handles sending messages via the Telegram Bot API."""
    def __init__(self, bot_token, chat_id):
        if not all([bot_token, chat_id]):
            raise ValueError("Telegram Bot Token or Chat ID is not configured.")
        
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
        logging.info("TelegramService initialized successfully.")

    async def send_message(self, message):
        """Sends a Markdown-formatted message to the configured chat."""
        logging.info("Attempting to send message to Telegram...")
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logging.info("Message sent successfully to Telegram.")
            return True
        except Exception as e:
            logging.error(f"Failed to send message to Telegram: {e}")
            return False