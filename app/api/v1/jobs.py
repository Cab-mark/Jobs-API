# jobs.py

from fastapi import APIRouter

# Initialize the router for jobs-related endpoints
router = APIRouter()

# Hardcoded job data
jobs_data = [
    {"job_id": "CSJ-0001", "job_title": "Senior Product Manager", "status": "Advertised", "views": 234},
    {"job_id": "CSJ-0002", "job_title": "Performance Analyst", "status": "Draft", "views": 0},
    {"job_id": "CSJ-0003", "job_title": "Service Designer", "status": "Advertised", "views": 178},
    {"job_id": "CSJ-0004", "job_title": "Interaction Designer", "status": "Closed", "views": 421},
    {"job_id": "CSJ-0005", "job_title": "Delivery Manager", "status": "Draft", "views": 0},
    {"job_id": "CSJ-0006", "job_title": "Technical Architect", "status": "Closed", "views": 355},
    {"job_id": "CSJ-0007", "job_title": "Recruitment Lead", "status": "Advertised", "views": 292},
]

# Define the GET endpoint
@router.get("/jobs")
def get_all_jobs():
    """
    Returns the complete list of mock job data.
    """
    # FastAPI automatically converts the Python list to a JSON response
    return jobs_data