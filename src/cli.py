
import argparse

from src.job_api import search_adzuna_jobs
from src.matcher import match_jobs
from src.resume_parser import extract_resume_text
from src.skill_extractor import extract_skills


def main():
    parser = argparse.ArgumentParser(
        description="Match your resume with job listings."
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
        help="Number of jobs to fetch (1-50)",
    )

    args = parser.parse_args()

    print("\nReading resume...")
    resume_text = extract_resume_text(args.resume)
    resume_skills = extract_skills(resume_text)

    print("Detected resume skills:", resume_skills)

    print("\nFetching jobs...")
    jobs = search_adzuna_jobs(
        query=args.query,
        location=args.location,
        results_per_page=args.limit,
    )

    if not jobs:
        print("No jobs found.")
        return

    results = match_jobs(resume_skills, jobs)

    print(f"\nFound {len(results)} jobs")
    print("=" * 60)

    for index, result in enumerate(results, start=1):
        print(f"\n{index}. {result['title']}")
        print(f"Match: {result['match_score']}%")
        print(f"Matched skills: {result['matched_skills']}")
        print(f"Missing skills: {result['missing_skills']}")

    print("\nMatching completed!")


if __name__ == "__main__":
    main()
