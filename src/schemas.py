from pydantic import BaseModel
from typing import Optional, List
import enum
from datetime import datetime

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    paused = "paused"
    finished = "finished"

# -----------------------------
#     CATEGORÍAS
# -----------------------------
class CategoryBase(BaseModel):
    name: str

# Clase para crear categoría
class CategoryCreate(CategoryBase):
    pass

# Clase para devolver categoría (lectura)
class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        # Pydantic v2: from_attributes reemplaza a orm_mode
        from_attributes = True

# -----------------------------
#       TAREAS
# -----------------------------
class TaskBase(BaseModel):
    title: str
    category_id: int

# Clase para crear tarea
class TaskCreate(TaskBase):
    pass

# Clase para devolver tarea (lectura)
class TaskOut(BaseModel):
    id: int
    title: str
    category_id: int
    time_spent: int
    status: TaskStatus
    current_start: int
    created_at: Optional[datetime] = None  # Fecha de creación
    finished_at: Optional[datetime] = None # Fecha de finalización

    # Para mostrar la categoría anidada
    category: Optional[CategoryOut] = None

    class Config:
        # Pydantic v2: from_attributes
        from_attributes = True