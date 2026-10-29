from pathlib import Path

from src.data_loader import load_jobs


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "examples"
    / "sample_jobs.json"
)


def test_load_jobs_returns_five_jobs():
    jobs = load_jobs(DATA_FILE)

    assert len(jobs) == 5
    assert jobs[0].job_id == "JOB001"
    assert jobs[0].title == "Junior Python Developer"


def test_loaded_jobs_are_job_objects():
    jobs = load_jobs(DATA_FILE)

    assert jobs[0].skills == ["Python", "SQL", "Git"]
    assert jobs[1].location == "Remote"


def test_optional_job_url_defaults_to_none():
    jobs = load_jobs(DATA_FILE)

    assert jobs[0].job_url is None
