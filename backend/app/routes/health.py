from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db


# Створюємо Blueprint
health_bp = Blueprint('health', __name__)


# --- Healthcheck для Docker ---
@health_bp.route("/full", methods=["GET"])
def health_readiness():
    try:
        # Проста перевірка підключення до БД
        db.session.execute(text("SELECT 1;"))
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 500
