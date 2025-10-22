from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

#Motor de conexion 
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

#Sesion de base de datos 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Clase base de modelos 
Base = declarative_base()