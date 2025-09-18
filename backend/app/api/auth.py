from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from app import models, schemas
from app.database.session import get_db
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["Users"])

# Crear usuario
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | 
        (models.User.email == user.email)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Crear hash de contraseña
    hashed_password = get_password_hash(user.password)
    
    # Crear nuevo usuario
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Obtener todos los usuarios
@router.get("/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Obtener usuario por ID
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

# Actualizar usuario
@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Lógica de autorización:
    # Un usuario solo puede modificarse a sí mismo, a menos que sea un superusuario.
    if db_user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to edit this user"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Verificar si el nuevo username o email ya están en uso por otro usuario
    if "username" in update_data and update_data["username"] != db_user.username:
        existing_user = db.query(models.User).filter(models.User.username == update_data["username"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

    if "email" in update_data and update_data["email"] != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == update_data["email"]).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar usuario
@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Lógica de autorización:
    # Un usuario solo puede eliminarse a sí mismo, a menos que sea un superusuario.
    if db_user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this user"
        )

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Endpoint de login
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}