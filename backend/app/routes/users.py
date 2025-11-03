from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import User


# Створюємо Blueprint
users_bp = Blueprint('users', __name__)


# Реєстрація користувача
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Валідація полів
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify(error), 400

    try:
        new_user = User(username=data["username"])
        new_user.set_password(data["password"])  # хешування пароля через метод класу

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user": new_user.to_dict()
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Авторизація користувача
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Перевірка наявності даних
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    user = db.session.query(User).filter_by(username=data["username"]).first()

    # Перевірка пароля
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Генерація JWT
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200


# "профільний" ендпоінт дозволяє користувачу отримати свої дані.
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = int(get_jwt_identity())
    user = db.session.get(User, current_user_id)
    return jsonify(user.to_dict())


# --- CRUD для User ---

# GET /users - отримання списку всіх користувачів.
@users_bp.route("", methods=["GET"])
@jwt_required()  # тільки авторизовані користувачі
def get_users():
    users = db.session.query(User).order_by(User.id).all()   # сортування по id
    return jsonify([serialize_user(u, include_tasks=False) for u in users])


# Так як додано новий едпоінт "/register" то даний едпоінт став не потрібним
# POST /users - створення нового користувача.
# @users_bp.route("", methods=["POST"])
# @jwt_required()
# def create_user():
#     data = request.get_json()
#     # Валідація полів
#     is_valid, error = validate_user_data(data)
#     if not is_valid:
#         return jsonify(error), 400
#
#     try:
#         new_user = User(username=data['username'], password=data['password'])
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(serialize_user(new_user)), 201
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500


# GET /users/:id - отримання інформації про конкретного користувача.
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": f"User with id {id} not found"}), 404

    return jsonify(user.to_dict())
    # return jsonify(serialize_user(user))


# PUT /users/:id - оновлення інформації про користувача.
@users_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    # Для редагування лише самого себе. Якщо потрібно логіку, то розкоментувати
    # current_user_id = int(get_jwt_identity())
    # if current_user_id != id:
    #     return jsonify({"error": "You can only update your own profile"}), 403

    data = request.get_json()
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": f"User with id {id} not found"}), 404

    # Валідація полів
    check_unique = 'username' in data and data['username'] != user.username
    is_valid, error = validate_user_data(data, check_username_unique=check_unique)
    if not is_valid:
        return jsonify(error), 400

    try:
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.set_password(data['password'])  # хешування пароля

        db.session.commit()
        return jsonify(user.to_dict())
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE /users/:id - видалення користувача.
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": f"User with id {id} not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User with id {id} deleted"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def serialize_user(user, include_tasks=True):
    """Перетворення моделі User у dict."""
    user_dict = {
        "id": user.id,
        "username": user.username,
    }

    if include_tasks:
        user_dict["tasks"] = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status
            }
            for t in sorted(user.tasks, key=lambda t: t.id)
        ]

    return user_dict


# Валідація полів на створення/оновлення користувача.
def validate_user_data(data, check_username_unique=True):
    """
    Перевіряє дані користувача.
    Повертає кортеж (is_valid: bool, error: dict)
    """
    if not data or not isinstance(data, dict):
        return False, {"error": "Request body must be a valid JSON object"}

    required_fields = ['username', 'password']
    missing_fields = [f for f in required_fields if f not in data]
    empty_fields = [f for f in required_fields if f in data and not data[f]]

    if missing_fields:
        return False, {"error": f"Missing required fields: {', '.join(missing_fields)}"}
    if empty_fields:
        return False, {"error": f"Fields cannot be empty: {', '.join(empty_fields)}"}

    # Перевірка унікальності username
    if check_username_unique:
        existing_user = db.session.query(User).filter_by(username=data['username']).first()
        if existing_user:
            return False, {"error": f"Username '{data['username']}' already exists"}

    return True, {}
