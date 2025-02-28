from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# QLAlchemy database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the news article model
class Article(Base):
    __tablename__ = "articles"

    title = Column(String, primary_key=True, index=True)
    link = Column(String, unique=True)

# Create the database tables
def create_database():
    Base.metadata.create_all(bind=engine)
