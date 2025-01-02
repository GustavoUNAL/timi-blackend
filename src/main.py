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
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     # Agrega dominios o puertos adicionales si tu front corre en otro lugar
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://3.128.32.128:3000", "https://timi-time.online"],  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir los routers de categorías y tareas
app.include_router(categories.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {APP_NAME}!"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)
