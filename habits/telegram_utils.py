from telegram import Bot
from telegram.error import TelegramError


def send_telegram_message(telegram_id, message):
    bot = Bot(token="YOUR_BOT_API_KEY")
    try:
        bot.send_message(chat_id=telegram_id, text=message)
    except TelegramError as e:
        print(f"Error sending message: {e}")
