
from src.skill_extractor import normalize_skill


def match_jobs(resume_skills: list[str], jobs: list) -> list[dict]:
    """Rank jobs by normalized resume skill overlap."""

    resume_set = {
        normalize_skill(skill).casefold()
        for skill in resume_skills
        if skill.strip()
    }

    results = []

    for job in jobs:
        required = []
        seen = set()

        for skill in job.skills:
            canonical = normalize_skill(skill)
            key = canonical.casefold()

            if key and key not in seen:
                seen.add(key)
                required.append(canonical)

        matched = [
            skill for skill in required
            if skill.casefold() in resume_set
        ]

        missing = [
            skill for skill in required
            if skill.casefold() not in resume_set
        ]

        score = (
            round(len(matched) / len(required) * 100, 2)
            if required else 0.0
        )

        results.append({
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        })

    return sorted(
        results,
        key=lambda result: result["match_score"],
        reverse=True,
    )
