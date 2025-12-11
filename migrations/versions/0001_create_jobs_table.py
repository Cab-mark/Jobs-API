"""Create jobs table aligned to jobs-data-contracts schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_jobs_table"
down_revision = None
branch_labels = None
depends_on = None


json_type = sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql")


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=False),
        sa.Column("approach", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("organisation", sa.String(), nullable=False),
        sa.Column("location", json_type, nullable=False),
        sa.Column("grade", sa.String(), nullable=False),
        sa.Column("assignment_type", sa.String(), nullable=False),
        sa.Column("work_location", json_type, nullable=False),
        sa.Column("working_pattern", json_type, nullable=False),
        sa.Column("personal_spec", sa.Text(), nullable=False),
        sa.Column("apply_detail", sa.Text(), nullable=False),
        sa.Column("date_posted", sa.DateTime(timezone=True), nullable=False),
        sa.Column("closing_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("profession", sa.String(), nullable=False),
        sa.Column("recruitment_email", sa.String(), nullable=False),
        sa.Column("contacts", json_type, nullable=True),
        sa.Column("nationality_requirement", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("apply_url", sa.String(), nullable=True),
        sa.Column("benefits", sa.Text(), nullable=True),
        sa.Column("salary", json_type, nullable=True),
        sa.Column("job_numbers", sa.Integer(), nullable=True),
        sa.Column("success_profile_details", sa.Text(), nullable=True),
        sa.Column("diversity_statement", sa.Text(), nullable=True),
        sa.Column("disability_confident", sa.Text(), nullable=True),
        sa.Column("dc_status", sa.String(), nullable=True),
        sa.Column("redeployment_scheme", sa.Text(), nullable=True),
        sa.Column("prison_scheme", sa.Text(), nullable=True),
        sa.Column("veteran_scheme", sa.Text(), nullable=True),
        sa.Column("criminal_record_check", sa.Text(), nullable=True),
        sa.Column("complaints_info", sa.Text(), nullable=True),
        sa.Column("working_for_the_civil_service", sa.Text(), nullable=True),
        sa.Column("eligibility_check", sa.Text(), nullable=True),
        sa.Column("attachments", json_type, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_jobs_external_id"), "jobs", ["external_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_external_id"), table_name="jobs")
    op.drop_table("jobs")
