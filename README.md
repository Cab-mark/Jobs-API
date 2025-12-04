# Jobs API Microservice (FastAPI)

A lightweight FastAPI microservice for listing and managing job postings with PostgreSQL database support. The job schema aligns with the TypeScript interface used in the nextjs_govuk_experiment (see active PR for details).

## Project Structure

```
Jobs-API-Microservice
├── app
│   ├── __init__.py
│   ├── main.py                # FastAPI app and router mounting
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   └── api
│       └── v1
│           └── jobs.py        # Jobs routes + Pydantic models
├── scripts
│   └── seed_db.py            # Database seeding script
├── Dockerfile                 # Docker image for API
├── docker-compose.yml         # Local development with Docker
├── .env.example              # Environment variables template
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Database Configuration

This application supports two database configurations:

- **Local Development**: PostgreSQL in Docker (via docker-compose)
- **Other Environments**: AWS RDS PostgreSQL (via environment variables)

The application uses the `DATABASE_URL` environment variable to connect to the database, making it easy to switch between environments.

## Setup Options

### Option 1: Docker (Recommended for Local Development)

This setup runs both the API and PostgreSQL database in Docker containers with persistent storage.

1) Clone the repository

```bash
git clone <repository-url>
cd Jobs-API-Microservice
```

2) Start the services with Docker Compose

```bash
docker-compose up -d
```

This will:
- Start a PostgreSQL database on port 5432 with persistent volume
- Build and start the API on port 8000
- Automatically create database tables on startup

3) (Optional) Seed the database with sample data

```bash
docker-compose exec api python scripts/seed_db.py
```

4) Access the API

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432 (credentials in docker-compose.yml)

5) Stop the services

```bash
docker-compose down
```

To remove the database volume (deletes all data):

```bash
docker-compose down -v
```

### Option 2: Local Python Setup (without Docker)

This setup requires a separate PostgreSQL instance.

1) Clone and enter the repo

```bash
git clone <repository-url>
cd Jobs-API-Microservice
```

2) Install dependencies (optionally in a virtualenv)

```bash
pip install -r requirements.txt
```

3) Set up database connection

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```
DATABASE_URL=postgresql://username:password@localhost:5432/jobsdb
```

4) Run the service

```bash
uvicorn app.main:app --reload
```

The app will be available at `http://127.0.0.1:8000`.

5) (Optional) Seed the database

```bash
python scripts/seed_db.py
```

## Deploying to AWS RDS

For staging/production environments using AWS RDS:

1) Create an RDS PostgreSQL instance in AWS

2) Set the `DATABASE_URL` environment variable in your deployment environment:

```bash
export DATABASE_URL=postgresql://username:password@your-rds-endpoint.region.rds.amazonaws.com:5432/jobsdb
```

For AWS services like ECS, Lambda, or Elastic Beanstalk, set this as an environment variable in the service configuration.

3) Deploy your application

The application will automatically:
- Connect to the RDS instance using the DATABASE_URL
- Create necessary tables on startup
- Use connection pooling for optimal performance

### Security Notes for AWS RDS

- Use AWS Secrets Manager or Parameter Store for database credentials
- Configure RDS security groups to allow connections only from your application
- Enable SSL/TLS for database connections in production
- Use IAM database authentication when possible

## API Overview

Current routes are mounted without a version prefix (base path is `/`). Endpoints exposed by `app/api/v1/jobs.py`:

- GET `/jobs` — list all jobs
- POST `/jobs` — create a new job (returns the created job with generated `id`)
- GET `/jobs/{job_id}` — fetch a single job by ID

If you prefer versioned paths (e.g., `/api/v1/jobs`), add a prefix when including the router in `app/main.py`.

## Data Model (summary)

The `Job` model includes (non-exhaustive):

- id, title, description, organisation, location, grade, assignmentType, personalSpec
- Optional: nationalityRequirement, summary, applyUrl, benefits, profession, applyDetail, salary, closingDate, jobNumbers
- contacts (bool), Optional: contactName, contactEmail, contactPhone
- recruitmentEmail

Example job object:

```json
{
   "id": "1567",
   "title": "Policy Advisor",
   "description": "This is a fantastic job for a policy advisor...",
   "organisation": "Ministry of Defence",
   "location": "3 Glass Wharf, Bristol, BS2 OEL",
   "grade": "Grade 7",
   "assignmentType": "Fixed Term Appointment (FTA)",
   "personalSpec": "Some personal specification text",
   "salary": "£45,000",
   "closingDate": "20 December 2025",
   "jobNumbers": 1,
   "contacts": false,
   "recruitmentEmail": "recruitment@civilservice.gov.uk"
}
```

## Quick Start (cURL)

- List jobs

```bash
curl -s "http://127.0.0.1:8000/jobs" | jq
```

- Create a job

```bash
curl -s -X POST "http://127.0.0.1:8000/jobs" \
   -H "Content-Type: application/json" \
   -d '{
      "title": "Backend Engineer",
      "description": "Build APIs with FastAPI.",
      "organisation": "Acme Corp",
      "location": "Remote",
      "grade": "Senior",
      "assignmentType": "Permanent",
      "personalSpec": "Python, FastAPI",
      "salary": "£100,000",
      "contacts": false,
      "recruitmentEmail": "talent@acme.example"
   }' | jq
```

- Get a job by ID

```bash
curl -s "http://127.0.0.1:8000/jobs/<job_id>" | jq
```

## Development

### Docker Development Workflow

The docker-compose setup includes hot-reloading for development:

1. Make changes to files in the `app/` directory
2. The API container will automatically reload
3. View logs: `docker-compose logs -f api`

### Database Management

- Connect to PostgreSQL: `docker-compose exec postgres psql -U jobsapi -d jobsdb`
- View logs: `docker-compose logs postgres`
- Reset database: `docker-compose down -v && docker-compose up -d`

## Environment Variables

| Variable | Description | Default (Local) | Production Example |
|----------|-------------|-----------------|-------------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://jobsapi:jobsapi@postgres:5432/jobsdb` | `postgresql://user:pass@rds-endpoint:5432/db` |

## License

MIT