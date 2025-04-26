from telegram import Bot
from django.conf import settings


class TelegramService:
    def __init__(self, bot_token=None):
        self.bot = Bot(token=bot_token or settings.TELEGRAM_API_KEY)

    def send_message(self, chat_id, text):
        try:
            self.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            print(f"Error sending message: {e}")


# Экземпляр бота
telegram_service = TelegramService()
