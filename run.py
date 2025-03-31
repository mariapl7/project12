from app import create_app
from bot.bot import start  # Импортируем функцию старта, если нужно

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    start()
