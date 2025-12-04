"""Script to seed the database with initial job data."""

import os
import sys

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, engine
from app.models import Base, JobModel

# Sample job data to seed the database
SEED_JOBS = [
    {
        "id": "1567",
        "title": "Policy Advisor",
        "description": "This is a fantastic job for a policy advisor...",
        "organisation": "Ministry of Defence",
        "location": "3 Glass Wharf, Bristol, BS2 OEL",
        "grade": "Grade 7",
        "assignment_type": "Fixed Term Appointment (FTA)",
        "personal_spec": "Some personal specification text",
        "salary": "£45,000",
        "closing_date": "20 December 2025",
        "job_numbers": 1,
        "contacts": False,
        "recruitment_email": "recruitment@civilservice.gov.uk"
    },
    {
        "id": "9488",
        "title": "Police Service - Volunteer Curator",
        "description": "This is a fantastic job for a curator...",
        "organisation": "College of Policing",
        "location": "2 Horse Guards, Whitehall, London, SW1A 2AX",
        "grade": "Grade 6",
        "assignment_type": "Permanent",
        "personal_spec": "Some personal specification text",
        "closing_date": "20 December 2025",
        "contacts": False,
        "recruitment_email": "recruitment@civilservice.gov.uk"
    },
    {
        "id": "9487",
        "title": "Project Manager",
        "description": "This is a fantastic job for a project manager...",
        "organisation": "Home Office",
        "location": "2 Horse Guards, Whitehall, London, SW1A 2AX",
        "grade": "Senior Executive Office",
        "assignment_type": "Fixed Term Appointment (FTA)",
        "personal_spec": "Some personal specification text",
        "salary": "£39,000 to £46,200",
        "closing_date": "20 December 2025",
        "contacts": False,
        "recruitment_email": "recruitment@civilservice.gov.uk"
    },
    {
        "id": "9489",
        "title": "Dentist",
        "description": "This is a fantastic job for a dentist...",
        "organisation": "HM Revenue and Customs",
        "location": "Benton Park Road, Newcastle upon Tyne, NE7 7LX",
        "grade": "Higher Executive Office",
        "assignment_type": "Apprenticeship",
        "personal_spec": "Some personal specification text",
        "salary": "£99,000",
        "closing_date": "5 January 2026",
        "contacts": False,
        "recruitment_email": "recruitment@civilservice.gov.uk"
    }
]


def seed_database():
    """Seed the database with initial job data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(JobModel).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} jobs. Skipping seed.")
            return
        
        print("Seeding database with initial job data...")
        for job_data in SEED_JOBS:
            job = JobModel(**job_data)
            db.add(job)
        
        db.commit()
        print(f"Successfully seeded {len(SEED_JOBS)} jobs!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
