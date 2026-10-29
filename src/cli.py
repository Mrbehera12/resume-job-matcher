
import argparse

from src.job_api import search_adzuna_jobs
from src.matcher import match_jobs
from src.resume_parser import extract_resume_text
from src.skill_extractor import extract_skills
from src.skill_recommender import recommend_skills


def main():
    parser = argparse.ArgumentParser(
        description="Match your resume with jobs and recommend missing skills."
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Path to your resume PDF",
    )

    parser.add_argument(
        "--query",
        required=True,
        help="Job search query",
    )

    parser.add_argument(
        "--location",
        default=None,
        help="Preferred job location",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        choices=range(1, 51),
        help="Number of jobs to fetch (1-50)",
    )

    args = parser.parse_args()

    # 1. Extract resume skills
    print("\n" + "=" * 65)
    print("RESUME-TO-JOB MATCHER")
    print("=" * 65)

    print("\n[1] Reading resume...")

    resume_text = extract_resume_text(args.resume)
    resume_skills = extract_skills(resume_text)

    print(f"\nDetected {len(resume_skills)} resume skills:")
    print(", ".join(resume_skills) if resume_skills else "No skills detected.")

    # 2. Fetch job listings
    print("\n[2] Fetching jobs...")

    jobs = search_adzuna_jobs(
        query=args.query,
        location=args.location,
        results_per_page=args.limit,
    )

    if not jobs:
        print("No jobs found. Check your search query or API configuration.")
        return

    print(f"Found {len(jobs)} jobs.")

    # 3. Match and rank jobs
    print("\n[3] Matching and ranking jobs...")

    results = match_jobs(resume_skills, jobs)

    print("\n" + "=" * 65)
    print("JOB MATCH RESULTS")
    print("Score = equal-weight detected skill coverage")
    print("=" * 65)

    for index, result in enumerate(results, start=1):
        print(f"\n{index}. {result['title']}")
        print(f"Company: {result['company']}")
        print(f"Match score: {result['match_score']:.2f}%")

        print(
            f"Skills matched: {result['matched_count']}/"
            f"{result['total_detected_skills']}"
        )

        if result["skill_data_status"] == "no_detected_skills":
            print("Skill data: Insufficient detected skills to assess.")
        else:
            print(f"Matched skills: {', '.join(result['matched_skills']) or 'None'}")
            print(f"Missing skills: {', '.join(result['missing_skills']) or 'None'}")

    # 4. Generate skill gap recommendations
    print("\n" + "=" * 65)
    print("SKILL GAP RECOMMENDATIONS")
    print("=" * 65)

    recommendations = recommend_skills(results, top_n=10)

    if not recommendations:
        print(
            "\nNo skill gap recommendations available "
            "from the detected job skills."
        )
    else:
        print("\nPrioritized skills to consider learning:\n")

        for index, item in enumerate(recommendations, start=1):
            print(f"{index}. {item['skill']}")
            print(f"   Requested by: {item['jobs_requesting']} jobs")
            print(f"   Job demand in this result set: {item['job_demand_percent']}%")

            titles = item.get("job_titles", [])
            if titles:
                print(f"   Relevant roles: {', '.join(titles)}")

            print()

    print("=" * 65)
    print("Matching and skill gap analysis completed!")
    print("=" * 65)

    print(
        "\nNote: Match scores reflect detected skill coverage, "
        "not hiring probability. Recommendations depend on "
        "the quality of skill extraction."
    )


if __name__ == "__main__":
    main()
