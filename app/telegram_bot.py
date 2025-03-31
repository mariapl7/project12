from telegram import Bot
from telegram.ext import Updater, CommandHandler
import logging
from datetime import datetime, timedelta
from app.models import db, Habit, HabitTracking

# Токен для твоего Telegram бота
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'  # id чата или пользователя для отправки сообщений

# Логирование ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для отправки напоминаний
def send_reminders(context):
    today = datetime.today().date()
    habits = Habit.query.all()

    for habit in habits:
        # Проверяем, была ли привычка выполнена
        last_tracking = HabitTracking.query.filter_by(habit_id=habit.id).order_by(HabitTracking.date.desc()).first()

        if last_tracking and last_tracking.date != today:
            message = f"Напоминаем о привычке: {habit.name}. Не забудь выполнить!"
            context.bot.send_message(chat_id=CHAT_ID, text=message)


# Токен, полученный от BotFather
TOKEN = 'your-telegram-bot-token'

# Инициализация бота
bot = Bot(token=TOKEN)

# Запуск бота
updater.start_polling()
updater.idle()


# Функция для старта бота
def start(update, context):
    update.message.reply_text("Привет! Я ваш бот для напоминаний.")


def send_reminder(update, context):
    chat_id = update.message.chat_id
    message = "Напоминание: пора выполнять привычку!"
    bot.send_message(chat_id=chat_id, text=message)

# Создание обработчика команд
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("remind", send_reminder))


# Основная функция для запуска Telegram бота
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрируем команду /start
    dp.add_handler(CommandHandler("start", start))

    # Настроим ежедневные напоминания
    job_queue = updater.job_queue
    job_queue.run_daily(send_reminders, time=datetime.time(hour=9, minute=0))  # Отправка в 9 утра

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
