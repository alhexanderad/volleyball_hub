
# from pydantic_settings import BaseSettings
# from pydantic import Field

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator

class Settings(BaseSettings):
    # La cadena de conexión para SQLite.
    # sqlite:///./test.db crea un archivo llamado test.db en el mismo directorio.
    DATABASE_URL: str = Field(default="sqlite:///./volley_stats.db", description="Database connection URL")
    SECRET_KEY: str = Field(default="tu-clave-secreta-muy-larga-y-segura", description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="Algorithm for JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration time in minutes")
    
    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES")
    def validate_expire_minutes(cls, v):
        if v <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer")
        return v
    
    class Config:
        env_file = ".env"
        extra = "ignore" # Ignorar variables de entorno adicionales no definidas en el modelo

settings = Settings()