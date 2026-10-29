
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
    assert results[0]["skill_data_status"] == "no_detected_skills"


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


def test_match_result_explains_score():
    jobs = [
        Job(
            job_id="JOB007",
            title="Python Developer",
            company="Example",
            description="",
            skills=["Python", "SQL", "Git", "React"],
        )
    ]

    results = match_jobs(["Python", "SQL", "Git"], jobs)
    result = results[0]

    assert result["match_score"] == 75.0
    assert result["matched_count"] == 3
    assert result["total_detected_skills"] == 4
    assert result["skill_data_status"] == "skills_detected"
    assert result["score_basis"] == (
        "Equal-weight detected skill coverage"
    )


def test_no_detected_skills_reports_insufficient_data():
    jobs = [
        Job(
            job_id="JOB008",
            title="General Role",
            company="Example",
            description="",
            skills=[],
        )
    ]

    results = match_jobs(["Python"], jobs)
    result = results[0]

    assert result["match_score"] == 0.0
    assert result["matched_count"] == 0
    assert result["total_detected_skills"] == 0
    assert result["skill_data_status"] == "no_detected_skills"


def test_ranking_prefers_more_matched_skills_when_scores_tie():
    jobs = [
        Job(
            job_id="JOB009",
            title="Python Developer",
            company="Example A",
            description="",
            skills=["Python"],
        ),
        Job(
            job_id="JOB010",
            title="Backend Developer",
            company="Example B",
            description="",
            skills=["Python", "SQL", "Git", "AWS"],
        ),
    ]

    results = match_jobs(
        ["Python", "SQL", "Git", "AWS"],
        jobs,
    )

    assert results[0]["job_id"] == "JOB010"
    assert results[1]["job_id"] == "JOB009"
    assert results[0]["match_score"] == 100.0
    assert results[1]["match_score"] == 100.0


def test_title_is_alphabetical_tiebreaker():
    jobs = [
        Job(
            job_id="JOB011",
            title="Python Developer",
            company="Example",
            description="",
            skills=["Python"],
        ),
        Job(
            job_id="JOB012",
            title="Backend Developer",
            company="Example",
            description="",
            skills=["Python"],
        ),
    ]

    results = match_jobs(["Python"], jobs)

    assert results[0]["title"] == "Backend Developer"
    assert results[1]["title"] == "Python Developer"
