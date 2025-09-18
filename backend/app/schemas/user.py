from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Esquema para crear usuario (sin ID)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Esquema para actualizar usuario
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

# Esquema para mostrar usuario (con ID)
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquema para respuesta de login
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None