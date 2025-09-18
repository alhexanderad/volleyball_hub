"""
Este módulo define el modelo de datos para la tabla 'users' en la base de datos.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    """
    Representa a un usuario en la base de datos.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    # No necesitamos relaciones en este modelo por ahora
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del objeto User.
        """
        return f"<User(username={self.username}, email={self.email})>"