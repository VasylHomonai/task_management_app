from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ForeignKey до таблиці User

    user = relationship("User", back_populates="tasks")
