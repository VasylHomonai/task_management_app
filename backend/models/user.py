from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import UniqueConstraint
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)  # Зберігає хеш пароля

    __table_args__ = (
        UniqueConstraint('username', name='unique_username'),
    )
