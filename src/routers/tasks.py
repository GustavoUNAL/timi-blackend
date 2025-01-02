from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload
import time
from datetime import datetime

from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Verifica que la categoría exista
    cat = db.query(models.Category).filter(models.Category.id == task.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Category does not exist.")

    db_task = models.Task(
        title=task.title,
        category_id=task.category_id,
        time_spent=0,
        status=models.TaskStatus.pending,
        current_start=0
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    # joinedload carga la relación Category para cada Task
    tasks = db.query(models.Task).options(joinedload(models.Task.category)).all()
    return tasks

@router.patch("/{task_id}/start")
def start_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    db_task.status = models.TaskStatus.in_progress
    db_task.current_start = int(time.time())
    db.commit()
    return {"message": "Task started"}

@router.patch("/{task_id}/pause")
def pause_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    if db_task.status == models.TaskStatus.in_progress:
        elapsed = int(time.time()) - db_task.current_start
        db_task.time_spent += elapsed
        db_task.current_start = 0
        db_task.status = models.TaskStatus.paused
        db.commit()
        return {"message": "Task paused"}
    raise HTTPException(status_code=400, detail="Task is not in progress.")

@router.patch("/{task_id}/finish")
def finish_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found.")

    # Si está en progreso, calculamos el tiempo adicional
    if db_task.status == models.TaskStatus.in_progress:
        elapsed = int(time.time()) - db_task.current_start
        db_task.time_spent += elapsed

    db_task.current_start = 0
    db_task.status = models.TaskStatus.finished
    db_task.finished_at = datetime.now()  # Establecer la fecha de finalización
    db.commit()
    db.refresh(db_task)

    return {"message": "Task finished", "task": db_task} 

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}
