from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import DB_URL

# connect_args = {"check_same_thread": False} es para SQLite y evitar errores
engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
