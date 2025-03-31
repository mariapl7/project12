from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Interval
from sqlalchemy.orm import relationship, validates
from app import db
from datetime import date


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Habit(db.Model):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)  # Действие привычки
    place = Column(String(200), nullable=False)  # Место выполнения
    time = Column(String(100), nullable=False)  # Время выполнения
    reward = Column(String(200), nullable=True)  # Вознаграждение
    execution_time = Column(Integer, nullable=False)  # Время на выполнение в минутах
    is_pleasant = Column(Boolean, default=False)  # Признак приятной привычки
    is_public = Column(Boolean, default=False)  # Признак публичности
    frequency = Column(Integer, default=1)  # Периодичность выполнения (по умолчанию 1 = ежедневно)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Связь с пользователем
    user = relationship('User', backref='habits')  # Обратная связь для пользователя

    # Связана ли привычка с другой привычкой
    linked_habit_id = Column(Integer, ForeignKey('habits.id'))
    linked_habit = relationship('Habit', remote_side=[id])

    created_at = Column(Integer, default=datetime.utcnow)

    @validates('reward', 'linked_habit_id')
    def validate_reward_and_linked_habit(self, key, value):
        """ Проверяем, что нельзя заполнить одновременно вознаграждение и связанную привычку """
        if key == 'reward' and self.linked_habit:
            raise ValueError("Нельзя указать и вознаграждение, и связанную привычку одновременно.")
        if key == 'linked_habit_id' and value and self.reward:
            raise ValueError("Нельзя указать и вознаграждение, и связанную привычку одновременно.")
        return value

    @validates('execution_time')
    def validate_execution_time(self, key, value):
        """ Время на выполнение не может быть больше 120 секунд """
        if value > 120:
            raise ValueError("Время на выполнение привычки не может быть больше 120 секунд.")
        return value

    @validates('linked_habit_id')
    def validate_linked_habit(self, key, value):
        """ Связанная привычка должна быть приятной привычкой """
        if value:
            linked_habit = Habit.query.get(value)
            if linked_habit and not linked_habit.is_pleasant:
                raise ValueError("Связанная привычка должна быть приятной.")
        return value

    @validates('reward')
    def validate_reward_for_pleasant_habit(self, key, value):
        """ Приятная привычка не может иметь вознаграждение """
        if self.is_pleasant and value:
            raise ValueError("Приятная привычка не может иметь вознаграждения.")
        return value

    @validates('frequency')
    def validate_frequency(self, key, value):
        """ Периодичность привычки не может быть меньше 1 раза в 7 дней """
        if value < 1:
            raise ValueError("Периодичность выполнения привычки не может быть меньше 1 раза в неделю.")
        return value

    @validates('frequency')
    def validate_max_frequency(self, key, value):
        """ Нельзя не выполнять привычку более 7 дней """
        if value > 7:
            raise ValueError("Периодичность привычки не может быть больше 7 дней.")
        return value

    def __repr__(self):
        return f"<Habit {self.name} - {self.place} - {self.time}>"

    def add_habit(user, name, place, time, reward, execution_time, is_pleasant=False, is_public=False, frequency=1,
                  linked_habit=None):
        new_habit = Habit(
            name=name,
            place=place,
            time=time,
            reward=reward,
            execution_time=execution_time,
            is_pleasant=is_pleasant,
            is_public=is_public,
            frequency=frequency,
            user=user,
            linked_habit=linked_habit
        )
        db.session.add(new_habit)
        db.session.commit()
        return new_habit


class HabitTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    status = db.Column(db.Boolean, nullable=False)  # True = выполнено, False = не выполнено

    def __repr__(self):
        return f'<HabitTracking {self.habit_id} on {self.date}>'
