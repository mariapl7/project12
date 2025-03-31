from celery import Celery

app = Celery('bot', broker='redis://localhost:6379/0')


class Bot:
    pass


@app.task
def send_telegram_reminder(chat_id, message):
    bot = Bot(token='your-telegram-bot-token')
    bot.send_message(chat_id=chat_id, text=message)
