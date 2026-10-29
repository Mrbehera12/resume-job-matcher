
from src.models import Job


def test_job_creation():
    job = Job(
        job_id="JOB001",
        title="Junior Python Developer",
        company="Example Tech",
        description="Build Python applications.",
        skills=["Python", "SQL", "Git"],
        location="Bengaluru",
    )

    assert job.job_id == "JOB001"
    assert job.title == "Junior Python Developer"
    assert job.skills == ["Python", "SQL", "Git"]


def test_job_optional_fields():
    job = Job(
        job_id="JOB002",
        title="Data Analyst",
        company="Sample Company",
        description="Analyze data.",
        skills=["SQL", "Python"],
    )

    assert job.location == "Not specified"
    assert job.job_url is None
