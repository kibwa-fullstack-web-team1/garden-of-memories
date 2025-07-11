from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv(
    "STORY_DATABASE_URL",
    "postgresql://neondb_owner:npg_JmHTASslW8B6@ep-summer-frost-a1ojuc9i-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 