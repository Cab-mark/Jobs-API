"""Database configuration and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable
# For local Docker: postgresql://jobsapi:jobsapi@postgres:5432/jobsdb
# For AWS RDS: postgresql://username:password@your-rds-endpoint:5432/dbname
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://jobsapi:jobsapi@postgres:5432/jobsdb"
)

# Create SQLAlchemy engine
# For production/AWS RDS, you might want to add connection pool settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enables connection health checks
    pool_size=10,  # Adjust based on your needs
    max_overflow=20,  # Maximum number of connections to create above pool_size
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
