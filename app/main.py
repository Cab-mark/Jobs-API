from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1.jobs import router as jobs_router
from app.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events."""
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Clean up resources if needed


app = FastAPI(lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})


app.include_router(jobs_router)


@app.get("/health")
async def health() -> dict:
    """Simple health endpoint. Returns 200 and minimal payload.

    Attempts a lightweight DB query; still returns ok on failure to avoid
    cascading outages during DB restarts.
    """
    status = {"status": "ok"}
    try:
        # Lazy import to avoid circulars and keep startup fast
        from app.database import SessionLocal

        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
            status["db"] = "ok"
    except Exception:
        status["db"] = "unavailable"
    return status


@app.get("/")
async def root() -> dict:
    """Basic landing endpoint with a pointer to interactive docs."""
    return {
        "service": "Jobs API",
        "status": "running",
        "message": "Welcome to the Jobs API. See interactive docs at /docs.",
        "docsUrl": "/docs",
    }
