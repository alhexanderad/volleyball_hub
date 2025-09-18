from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base import Base

# Cadena de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# SQLite no soporta hilos múltiples. Agrega check_same_thread=False.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # Solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()