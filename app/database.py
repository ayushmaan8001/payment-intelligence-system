import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST', 'localhost')

DATABASE_URL = f"mysql+pymysql://root:{db_password}@{db_host}/payment_intelligence"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()