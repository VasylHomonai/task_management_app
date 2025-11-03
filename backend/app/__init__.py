from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import text
import os, time


db = SQLAlchemy()
jwt = JWTManager()  # створюємо JWT менеджер


def create_app():
    app = Flask(__name__)

    # --- Конфігурація ---
    database_url = os.getenv('DATABASE_URL') or 'sqlite:///:memory:'

    # Беремо URL з .env (передається в контейнер через env_file)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'very_secret_key')

    # --- Ініціалізація ---
    db.init_app(app)
    jwt.init_app(app)
    # Дозволяємо запити з фронта (localhost:3000)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # --- Retry логіка перед create_all ---
    retries = 10  # скільки разів спробувати
    delay = 5     # секунд між спробами

    for attempt in range(1, retries + 1):
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))  # Перевірка підключення
            print("✅ Database connected successfully and tables created.")
            break
        except Exception as e:
            print(f"⚠️ Database connection failed (attempt {attempt}/{retries}): {e}")
            if attempt == retries:
                raise
            time.sleep(delay)

    # --- Реєстрація Blueprint ---
    from .routes import register_blueprints
    register_blueprints(app)

    return app
