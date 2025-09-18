"""
Este módulo define la base declarativa para los modelos de SQLAlchemy.
Todos los modelos de la aplicación deben heredar de esta clase Base.
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()