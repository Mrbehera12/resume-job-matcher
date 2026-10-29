
from src.skill_extractor import normalize_skill


def match_jobs(resume_skills: list[str], jobs: list) -> list[dict]:
    """Match resume skills with jobs and rank the results."""

    # Normalize resume skills and remove duplicates
    resume_set = {
        normalize_skill(skill).casefold()
        for skill in resume_skills
        if skill.strip()
    }

    results = []

    for job in jobs:
        required = []
        seen = set()

        # Normalize job skills and remove duplicates
        for skill in job.skills:
            canonical = normalize_skill(skill)
            key = canonical.casefold()

            if key and key not in seen:
                seen.add(key)
                required.append(canonical)

        # Identify matched skills
        matched = [
            skill for skill in required
            if skill.casefold() in resume_set
        ]

        # Identify missing skills
        missing = [
            skill for skill in required
            if skill.casefold() not in resume_set
        ]

        matched_count = len(matched)
        total_detected = len(required)

        # Calculate detected skill coverage
        score = (
            round(matched_count / total_detected * 100, 2)
            if total_detected else 0.0
        )

        results.append({
            "job_id": job.job_id,
            "title": job.title,
            "company": job.company,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "matched_count": matched_count,
            "total_detected_skills": total_detected,
            "skill_data_status": (
                "skills_detected"
                if total_detected
                else "no_detected_skills"
            ),
            "score_basis": "Equal-weight detected skill coverage",
        })

    # Rank by coverage, matched skill count, then title
    return sorted(
        results,
        key=lambda result: (
            -result["match_score"],
            -result["matched_count"],
            result["title"].casefold(),
        ),
    )
