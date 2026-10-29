
from src.models import Job


job = Job(
    job_id="JOB001",
    title="Junior Python Developer",
    company="Example Tech",
    description=(
        "Develop Python applications, write SQL queries, "
        "use Git and collaborate with developers."
    ),
    skills=["Python", "SQL", "Git"],
    location="Bengaluru",
)

print(job)
print("\nJob title:", job.title)
print("Required skills:", job.skills)
