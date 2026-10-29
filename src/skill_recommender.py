from collections import Counter, defaultdict


def recommend_skills(match_results: list[dict], top_n: int = 10) -> list[dict]:
    """Rank missing skills by how many analyzable jobs request them.

    Jobs with no detected skills are excluded. Each job contributes at most
    once per skill. The percentage is within the supplied job result set,
    not a market-wide demand estimate.
    """
    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    analyzable_jobs = 0
    demand = Counter()
    titles_by_skill = defaultdict(list)

    for result in match_results:
        if result.get("skill_data_status") == "no_detected_skills":
            continue

        # Accept older result dictionaries, too.
        if "skill_data_status" not in result and not result.get(
            "total_detected_skills", 0
        ):
            continue

        analyzable_jobs += 1
        seen_in_job = set()

        for skill in result.get("missing_skills", []):
            if not isinstance(skill, str):
                continue
            skill = skill.strip()
            if not skill:
                continue

            key = skill.casefold()
            if key in seen_in_job:
                continue
            seen_in_job.add(key)
            demand[key] += 1

            title = result.get("title", "Untitled role")
            if title not in titles_by_skill[key]:
                titles_by_skill[key].append(title)

    # Keep a display label for each normalized key.
    labels = {}
    for result in match_results:
        for skill in result.get("missing_skills", []):
            if isinstance(skill, str) and skill.strip():
                labels.setdefault(skill.strip().casefold(), skill.strip())

    ranked = sorted(
        demand,
        key=lambda key: (-demand[key], labels[key].casefold()),
    )

    return [
        {
            "skill": labels[key],
            "jobs_requesting": demand[key],
            "job_demand_percent": round(
                demand[key] / analyzable_jobs * 100, 2
            ) if analyzable_jobs else 0.0,
            "job_titles": titles_by_skill[key],
        }
        for key in ranked[:top_n]
    ]
