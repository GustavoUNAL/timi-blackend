from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    paused = "paused"
    finished = "finished"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relación 1-N: una categoría tiene muchas tareas
    tasks = relationship("Task", back_populates="category")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    time_spent = Column(Integer, default=0)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    current_start = Column(Integer, default=0)

    # Relación inversa: una tarea pertenece a una categoría
    category = relationship("Category", back_populates="tasks")
