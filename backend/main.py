from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth as users
from app.database.session import engine
from app.models.base import Base
from app.core.config import settings

# Crear tablas de base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VolleyStats API",
    description="API para gestión de jugadores de voleibol",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router, prefix="/api", tags=["Users"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a VolleyStats API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}