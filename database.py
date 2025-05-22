from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Настройка базы данных
engine = create_engine("sqlite:///./db.sqlite", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Таблица для хранения URL
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True)
    short_id = Column(String(10), unique=True)
    original_url = Column(String)

Base.metadata.create_all(bind=engine)