import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

try:
    connection = engine.connect()
    print("Соединение с базой данных установлено")
    connection.close()
except Exception as e:
    print(f"Ошибка соединения с базой данных: {e}")

def get_session():
    with session_factory() as session:
        yield session