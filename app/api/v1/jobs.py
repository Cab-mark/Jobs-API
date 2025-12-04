# jobs.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from datetime import date

from app.database import get_db
from app.models import JobModel

# --- 1. Define the Pydantic Schema matching TypeScript Job interface ---
# This schema matches the Job interface from nextjs_govuk_experiment repository
class Job(BaseModel):
    """
    Job schema matching the TypeScript interface from nextjs_govuk_experiment.
    """
    id: str
    title: str
    description: str
    organisation: str
    location: str
    grade: str
    assignmentType: str
    personalSpec: str
    nationalityRequirement: Optional[str] = None
    summary: Optional[str] = None
    applyUrl: Optional[str] = None
    benefits: Optional[str] = None
    profession: Optional[str] = None
    applyDetail: Optional[str] = None
    salary: Optional[str] = None
    closingDate: Optional[str] = None
    jobNumbers: Optional[int] = None
    contacts: bool
    contactName: Optional[str] = None
    contactEmail: Optional[str] = None
    contactPhone: Optional[str] = None
    recruitmentEmail: str

# --- 2. Define the Pydantic Schema for Job POST Data ---
# This class defines the structure for creating new jobs (without the auto-generated id)
class JobPost(BaseModel):
    """
    Schema for a new job post request (without id field).
    """
    title: str
    description: str
    organisation: str
    location: str
    grade: str
    assignmentType: str
    personalSpec: str
    nationalityRequirement: Optional[str] = None
    summary: Optional[str] = None
    applyUrl: Optional[str] = None
    benefits: Optional[str] = None
    profession: Optional[str] = None
    applyDetail: Optional[str] = None
    salary: Optional[str] = None
    closingDate: Optional[str] = None
    jobNumbers: Optional[int] = None
    contacts: bool = False
    contactName: Optional[str] = None
    contactEmail: Optional[str] = None
    contactPhone: Optional[str] = None
    recruitmentEmail: str

# --- 3. Initialize Router ---

# Initialize the router for jobs-related endpoints
router = APIRouter()

# --- 4. Helper function to convert JobModel to Job dict ---

def job_model_to_dict(job_model: JobModel) -> dict:
    """Convert SQLAlchemy JobModel to dict matching the Job Pydantic model."""
    return {
        "id": job_model.id,
        "title": job_model.title,
        "description": job_model.description,
        "organisation": job_model.organisation,
        "location": job_model.location,
        "grade": job_model.grade,
        "assignmentType": job_model.assignment_type,
        "personalSpec": job_model.personal_spec,
        "nationalityRequirement": job_model.nationality_requirement,
        "summary": job_model.summary,
        "applyUrl": job_model.apply_url,
        "benefits": job_model.benefits,
        "profession": job_model.profession,
        "applyDetail": job_model.apply_detail,
        "salary": job_model.salary,
        "closingDate": job_model.closing_date,
        "jobNumbers": job_model.job_numbers,
        "contacts": job_model.contacts,
        "contactName": job_model.contact_name,
        "contactEmail": job_model.contact_email,
        "contactPhone": job_model.contact_phone,
        "recruitmentEmail": job_model.recruitment_email,
    }

# --- 5. GET all jobs endpoint ---

@router.get("/jobs", response_model=List[Job])
def get_all_jobs(db: Session = Depends(get_db)):
    """
    Returns the complete list of jobs from the database.
    """
    jobs = db.query(JobModel).all()
    return [job_model_to_dict(job) for job in jobs]

# --- 6. POST endpoint to create a new job ---

@router.post("/jobs", response_model=Job, status_code=201)
def create_job(job: JobPost, db: Session = Depends(get_db)):
    """
    Accepts a new job post and adds it to the database.
    """
    # Generate a unique ID for the new job
    new_id = f"CSJ-{str(uuid.uuid4())[:8].upper()}"
    
    # Create the JobModel instance
    new_job = JobModel(
        id=new_id,
        title=job.title,
        description=job.description,
        organisation=job.organisation,
        location=job.location,
        grade=job.grade,
        assignment_type=job.assignmentType,
        personal_spec=job.personalSpec,
        nationality_requirement=job.nationalityRequirement,
        summary=job.summary,
        apply_url=job.applyUrl,
        benefits=job.benefits,
        profession=job.profession,
        apply_detail=job.applyDetail,
        salary=job.salary,
        closing_date=job.closingDate,
        job_numbers=job.jobNumbers,
        contacts=job.contacts,
        contact_name=job.contactName,
        contact_email=job.contactEmail,
        contact_phone=job.contactPhone,
        recruitment_email=job.recruitmentEmail,
    )
    
    # Add the new job to the database
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # Return the created job object
    return job_model_to_dict(new_job)

# --- 7. GET single job by ID endpoint ---

@router.get("/jobs/{job_id}", response_model=Job)
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieves a single job based on its unique job ID.
    """
    # Query the database for the job with the matching ID
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    
    if job is None:
        # If no job is found, raise a 404 exception
        raise HTTPException(status_code=404, detail=f"Job with ID '{job_id}' not found")
    
    return job_model_to_dict(job)