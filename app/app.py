from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask import Flask
from flask_cors import CORS

# Создаем экземпляры приложения и базы данных
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Модели для базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# Главная точка входа
@app.route('/')
def home():
    return "Hello, Habit Tracker!"

app = Flask(__name__)

# Настройка CORS для всех доменов
CORS(app)

# Или настройка CORS для конкретных доменов:
# CORS(app, resources={r"/api/*": {"origins": "https://your-frontend-domain.com"}})

@app.route('/api/your-endpoint')
def your_endpoint():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)





