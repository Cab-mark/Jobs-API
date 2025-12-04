from fastapi import FastAPI
from app.api.v1.jobs import router as jobs_router
from app.database import engine
from app.models import Base

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    """Create database tables on application startup."""
    Base.metadata.create_all(bind=engine)

app.include_router(jobs_router)