from fastapi import FastAPI
from app.api.v1.jobs import router as jobs_router

app = FastAPI()

app.include_router(jobs_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the mock jobs API microservice"}