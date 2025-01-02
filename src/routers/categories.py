from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/categories", tags=["categories"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CategoryOut)
def create_category(cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # Crea una nueva categoría
    db_cat = models.Category(name=cat.name)
    db.add(db_cat)
    try:
        db.commit()
        db.refresh(db_cat)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category already exists or invalid.")
    return db_cat

@router.get("/", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.delete("/{cat_id}")
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found.")
    db.delete(db_cat)
    db.commit()
    return {"message": "Category deleted"}
