import os
from dotenv import load_dotenv

# Carga el contenido de .env
load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///./timi.db")
APP_NAME = os.getenv("APP_NAME", "Timi")
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
