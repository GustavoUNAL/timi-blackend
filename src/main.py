import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import APP_NAME, DEBUG_MODE
from .database import engine
from .models import Base
from .routers import categories, tasks

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, debug=DEBUG_MODE)

# Configurar CORS (ajusta según tus necesidades)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(categories.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {APP_NAME}!"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
