from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import Task, User


# Створюємо Blueprint
tasks_bp = Blueprint('tasks', __name__)


# --- CRUD для Task ---

# GET /tasks - отримання списку всіх задач, для авторизованих користувачів.
# Будь-який авторизований користувач може подивитись список всіх задач, всіх користувачів
@tasks_bp.route("", methods=["GET"])
@jwt_required()  # тільки авторизовані користувачі
def get_tasks():
    tasks = db.session.query(Task).order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks])


# GET /tasks - отримання списку всіх задач, для не авторизованого користувача.
# Зроблено для WEB, щоб сторінка отримувала всі задачі
@tasks_bp.route("/public", methods=["GET"])
def get_tasks_public():
    tasks = db.session.query(Task).order_by(Task.id).all()
    return jsonify([task.to_dict() for task in tasks])


# GET /tasks - отримання списку всіх задач даного авторизованого користувача.
# Будь-який авторизований користувач може подивитись список всіх своїх задач.
# @tasks_bp.route("", methods=["GET"])
# @jwt_required()
# def get_tasks():
#     current_user_id = int(get_jwt_identity())
#     tasks = Task.query.filter_by(owner_id=current_user_id).order_by(Task.id).all()
#     return jsonify([task.to_dict() for task in tasks])


# POST /tasks - створення нової задачі на будь-якого зареєстрованого користувача.
@tasks_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    # Валідація обов'язкових полів
    is_valid, error = validate_task_data(data, check_owner_exists=True)
    if not is_valid:
        return jsonify(error), 400

    try:
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            owner_id=data['owner_id'],
            status=data.get('status', "невиконана")
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# GET /tasks/:id - отримання інформації про конкретну задачу.
@tasks_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    task = db.session.get(Task, id)
    if not task:
        return jsonify({"error": f"Task with id {id} not found"}), 404
    return jsonify(task.to_dict())


# PUT /tasks/:id - оновлення інформації про задачу.
@tasks_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    data = request.get_json()
    task = db.session.get(Task, id)
    if not task:
        return jsonify({"error": f"Task with id {id} not found"}), 404

    # Перевіряємо owner_id лише якщо він переданий
    check_owner = 'owner_id' in data
    is_valid, error = validate_task_data(data, check_owner_exists=check_owner, require_all_fields=False)
    if not is_valid:
        return jsonify(error), 400

    try:
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'owner_id' in data:
            task.owner_id = data['owner_id']

        db.session.commit()
        return jsonify(task.to_dict())
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# DELETE /tasks/:id - видалення задачі.
@tasks_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = db.session.get(Task, id)

    if not task:
        return jsonify({"error": f"Task with id {id} not found"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({}), 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Валідація полів на створення/оновлення задачі.
def validate_task_data(data, check_owner_exists=True, require_all_fields=True):
    """
    Перевірка даних для Task.
    Повертає кортеж:
        - (True, {}) якщо дані валідні
        - (False, {"error": "..."}) якщо невалідні
    """
    if not data or not isinstance(data, dict):
        return False, {"error": "Request body must be a valid JSON object"}

    # Перевірка обов'язкових полів
    required_fields = ['title', 'owner_id']

    if require_all_fields:
        missing_fields = [f for f in required_fields if f not in data]
        empty_fields = [f for f in required_fields if f in data and not data[f]]

        if missing_fields:
            return False, {"error": f"Missing required fields: {', '.join(missing_fields)}"}
        if empty_fields:
            return False, {"error": f"Fields cannot be empty: {', '.join(empty_fields)}"}

    # Перевірка чи існує користувач з owner_id
    if 'owner_id' in data and check_owner_exists:
        try:
            owner_id = int(data['owner_id'])
        except (ValueError, TypeError):
            return False, {"error": "owner_id must be a valid integer"}

        owner = db.session.get(User, owner_id)
        if not owner:
            return False, {"error": f"User with id {owner_id} does not exist"}

        data['owner_id'] = owner_id  # зберігаємо як int

    return True, {}
