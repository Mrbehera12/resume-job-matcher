
import json
from pathlib import Path

from src.models import Job


def load_jobs(file_path: str | Path) -> list[Job]:
    """Load job postings from a JSON file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Job dataset must contain a JSON list")

    jobs = []

    for record in records:
        job = Job(
            job_id=record["job_id"],
            title=record["title"],
            company=record["company"],
            description=record["description"],
            skills=record["skills"],
            location=record.get("location", "Not specified"),
            job_url=record.get("job_url"),
        )
        jobs.append(job)

    return jobs
