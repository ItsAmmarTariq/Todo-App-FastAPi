from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from application.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,nullable=False)  
    username = Column(String, index=True, unique=True,nullable=False)
    email = Column(String, index=True, unique=True,nullable=False)
    hashed_password = Column(String)

    # One-to-Many relationship with Todo
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String,nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow)
    due_date = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
