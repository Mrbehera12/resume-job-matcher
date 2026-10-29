
from src.matcher import match_jobs
from src.models import Job
from src.skill_extractor import extract_skills

def test_duplicate_skills_ignore_case():
    jobs = [
        Job(
            job_id="JOB003",
            title="Python Developer",
            company="Example",
            description="",
            skills=["Python", "python", "SQL"],
        )
    ]

    results = match_jobs(["Python", "SQL"], jobs)

    assert results[0]["match_score"] == 100.0
    assert results[0]["matched_skills"] == ["Python", "SQL"]
    assert results[0]["missing_skills"] == []


def test_job_with_no_required_skills_has_zero_score():
    jobs = [
        Job(
            job_id="JOB004",
            title="General Role",
            company="Example",
            description="",
            skills=[],
        )
    ]

    results = match_jobs(["Python"], jobs)

    assert results[0]["match_score"] == 0.0
    assert results[0]["matched_skills"] == []
    assert results[0]["missing_skills"] == []


def test_duplicate_resume_skills_do_not_inflate_score():
    jobs = [
        Job(
            job_id="JOB005",
            title="Python Developer",
            company="Example",
            description="",
            skills=["Python", "SQL"],
        )
    ]

    results = match_jobs(["Python", "Python", "SQL"], jobs)

    assert results[0]["match_score"] == 100.0


def test_aliases_match_canonical_job_skills():
    resume_skills = extract_skills(
        "I have experience with Postgres and Node JS."
    )

    jobs = [
        Job(
            job_id="JOB006",
            title="Backend Developer",
            company="Example",
            description="",
            skills=["PostgreSQL", "Node.js"],
        )
    ]

    results = match_jobs(resume_skills, jobs)

    assert results[0]["match_score"] == 100.0
    assert results[0]["matched_skills"] == [
        "PostgreSQL",
        "Node.js",
    ]
    assert results[0]["missing_skills"] == []
