
from src.data_loader import load_jobs


def main():
    jobs = load_jobs("data/examples/sample_jobs.json")

    print("Total jobs loaded:", len(jobs))
    print()

    for job in jobs:
        print(f"{job.job_id} | {job.title} | {job.location}")


if __name__ == "__main__":
    main()
