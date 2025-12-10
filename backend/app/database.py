"""
Database Configuration and Session Management
Supports both PostgreSQL and SQLite
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Get database URL from settings
database_url = settings.DATABASE_URL

# Determine database type and create appropriate engine
if database_url.startswith("sqlite"):
    # SQLite configuration (for development)
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        echo=False
    )
    print("📦 Using SQLite database")
else:
    # PostgreSQL configuration (for production)
    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
    print("🐘 Using PostgreSQL database")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    """
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
