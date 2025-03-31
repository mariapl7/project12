from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Habit, HabitTracking
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

bp = Blueprint('api', __name__)


# Регистрация пользователя
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Проверка наличия пользователя с таким же email
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "User already exists!"}), 400

    # Хэширование пароля
    hashed_password = generate_password_hash(data['password'])

    # Создание нового пользователя
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Вход пользователя (получение JWT токена)
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Проверка существования пользователя
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials!"}), 401

    # Создание токена
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200


# Получение всех привычек для пользователя
@bp.route('/habits', methods=['GET'])
@jwt_required()
def get_habits():
    user_id = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    habits_query = Habit.query.filter_by(user_id=user_id).paginate(page, per_page, False)
    habits = habits_query.items
    total_pages = habits_query.pages
    current_page = habits_query.page

    habits_list = [{
        'id': habit.id,
        'name': habit.name,
        'place': habit.place,
        'time': habit.time,
        'reward': habit.reward,
        'execution_time': habit.execution_time,
        'is_pleasant': habit.is_pleasant,
        'linked_habit': habit.linked_habit.id if habit.linked_habit else None
    } for habit in habits]

    return jsonify({
        'habits': habits_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total_items': habits_query.total
    })


# Отслеживание выполнения привычки
@bp.route('/habits/<int:habit_id>/track', methods=['POST'])
@jwt_required()
def track_habit(habit_id):
    user_id = get_jwt_identity()
    habit = Habit.query.get(habit_id)

    if habit is None or habit.user_id != user_id:
        return jsonify({'message': 'Habit not found or unauthorized'}), 404

    data = request.get_json()
    tracking = HabitTracking(habit_id=habit.id, status=data['status'])

    try:
        db.session.add(tracking)
        db.session.commit()
        return jsonify({'message': 'Tracking updated'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Error during tracking'}), 500


# Получение списка привычек с пагинацией
@bp.route('/habits', methods=['GET'])
@jwt_required()
def get_habits():
    user_id = get_jwt_identity()

    # Получаем параметры пагинации из запроса (по умолчанию 1 страница и 5 привычек на страницу)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Получаем привычки для данного пользователя с пагинацией
    habits_query = Habit.query.filter_by(user_id=user_id).paginate(page, per_page, False)

    # Составляем результат
    habits = habits_query.items
    total_pages = habits_query.pages
    current_page = habits_query.page

    # Формируем список привычек для ответа
    habits_list = [{
        'id': habit.id,
        'name': habit.name,
        'place': habit.place,
        'time': habit.time,
        'reward': habit.reward,
        'execution_time': habit.execution_time,
        'is_pleasant': habit.is_pleasant,
        'linked_habit': habit.linked_habit.id if habit.linked_habit else None
    } for habit in habits]

    # Возвращаем ответ с пагинацией
    return jsonify({
        'habits': habits_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total_items': habits_query.total
    })


@bp.route('/public_habits', methods=['GET'])
def get_public_habits():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    habits_query = Habit.query.filter_by(is_public=True).paginate(page, per_page, False)
    habits = habits_query.items
    total_pages = habits_query.pages
    current_page = habits_query.page

    habits_list = [{
        'id': habit.id,
        'name': habit.name,
        'place': habit.place,
        'time': habit.time,
        'reward': habit.reward,
        'execution_time': habit.execution_time,
        'is_pleasant': habit.is_pleasant,
        'linked_habit': habit.linked_habit.id if habit.linked_habit else None
    } for habit in habits]

    return jsonify({
        'habits': habits_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total_items': habits_query.total
    })


@bp.route('/public_habits', methods=['GET'])
def get_public_habits():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    habits_query = Habit.query.filter_by(is_public=True).paginate(page, per_page, False)
    habits = habits_query.items
    total_pages = habits_query.pages
    current_page = habits_query.page

    habits_list = [{
        'id': habit.id,
        'name': habit.name,
        'place': habit.place,
        'time': habit.time,
        'reward': habit.reward,
        'execution_time': habit.execution_time,
        'is_pleasant': habit.is_pleasant,
        'linked_habit': habit.linked_habit.id if habit.linked_habit else None
    } for habit in habits]

    return jsonify({
        'habits': habits_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total_items': habits_query.total
    })


# Добавление новой привычки
@bp.route('/habits', methods=['POST'])
@jwt_required()
def add_new_habit():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_habit = Habit(
        name=data['name'],
        place=data['place'],
        time=data['time'],
        reward=data.get('reward'),
        execution_time=data['execution_time'],
        is_pleasant=data.get('is_pleasant', False),
        is_public=data.get('is_public', False),
        user_id=user_id
    )

    try:
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({'message': 'Habit added successfully', 'habit': new_habit.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@bp.route('/habits/<int:habit_id>', methods=['DELETE'])
@jwt_required()
def delete_habit(habit_id):
    user_id = get_jwt_identity()
    habit = Habit.query.get_or_404(habit_id)

    if habit.user_id != user_id:
        return jsonify({'message': 'You can only delete your own habits!'}), 403

    db.session.delete(habit)
    db.session.commit()

    return jsonify({'message': 'Habit deleted successfully'}), 200


@bp.route('/habits/<int:habit_id>', methods=['PUT'])
@jwt_required()
def update_habit(habit_id):
    user_id = get_jwt_identity()
    habit = Habit.query.get_or_404(habit_id)

    if habit.user_id != user_id:
        return jsonify({'message': 'You can only update your own habits!'}), 403

    data = request.get_json()

    habit.name = data.get('name', habit.name)
    habit.place = data.get('place', habit.place)
    habit.time = data.get('time', habit.time)
    habit.reward = data.get('reward', habit.reward)
    habit.execution_time = data.get('execution_time', habit.execution_time)
    habit.is_pleasant = data.get('is_pleasant', habit.is_pleasant)
    habit.is_public = data.get('is_public', habit.is_public)

    db.session.commit()

    return jsonify({'message': 'Habit updated successfully'}), 200
