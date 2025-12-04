"""SQLAlchemy models for the Jobs API."""

from sqlalchemy import Column, String, Boolean, Integer
from app.database import Base


class JobModel(Base):
    """SQLAlchemy model for Job table."""
    
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    organisation = Column(String, nullable=False)
    location = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    assignment_type = Column(String, nullable=False)
    personal_spec = Column(String, nullable=False)
    nationality_requirement = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    apply_url = Column(String, nullable=True)
    benefits = Column(String, nullable=True)
    profession = Column(String, nullable=True)
    apply_detail = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    closing_date = Column(String, nullable=True)
    job_numbers = Column(Integer, nullable=True)
    contacts = Column(Boolean, nullable=False, default=False)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    recruitment_email = Column(String, nullable=False)
