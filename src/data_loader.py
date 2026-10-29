
import json
from pathlib import Path

from src.models import Job


REQUIRED_FIELDS = {
    "job_id",
    "title",
    "company",
    "description",
    "skills",
}


def validate_job_record(record: object, index: int) -> None:
    """Validate one job record."""
    if not isinstance(record, dict):
        raise ValueError(f"Job at index {index} must be an object")

    missing = REQUIRED_FIELDS - record.keys()

    if missing:
        raise ValueError(
            f"Job at index {index} is missing fields: "
            f"{sorted(missing)}"
        )

    for field in ("job_id", "title", "company", "description"):
        value = record[field]

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Job at index {index}: "
                f"'{field}' must be a non-empty string"
            )

    skills = record["skills"]

    if not isinstance(skills, list):
        raise ValueError(
            f"Job at index {index}: 'skills' must be a list"
        )

    if any(
        not isinstance(skill, str) or not skill.strip()
        for skill in skills
    ):
        raise ValueError(
            f"Job at index {index}: "
            "'skills' must contain non-empty strings"
        )

    location = record.get("location", "Not specified")

    if not isinstance(location, str) or not location.strip():
        raise ValueError(
            f"Job at index {index}: "
            "'location' must be a non-empty string"
        )

    job_url = record.get("job_url")

    if job_url is not None and not isinstance(job_url, str):
        raise ValueError(
            f"Job at index {index}: 'job_url' must be a string or null"
        )


def load_jobs(file_path: str | Path) -> list[Job]:
    """Load and validate job postings from a JSON file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Job dataset must contain a JSON list")

    jobs = []
    seen_ids = set()

    for index, record in enumerate(records):
        validate_job_record(record, index)

        job_id = record["job_id"].strip()

        if job_id in seen_ids:
            raise ValueError(f"Duplicate job_id: {job_id}")

        seen_ids.add(job_id)

        job = Job(
            job_id=job_id,
            title=record["title"].strip(),
            company=record["company"].strip(),
            description=record["description"].strip(),
            skills=[skill.strip() for skill in record["skills"]],
            location=record.get("location", "Not specified").strip(),
            job_url=record.get("job_url"),
        )
        jobs.append(job)

    return jobs
