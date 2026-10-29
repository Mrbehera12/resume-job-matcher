
from dataclasses import dataclass

@dataclass
class Job:
    job_id: str
    title: str
    company: str
    description: str
    skills: list[str]
    location: str = "Not specified"
    job_url: str | None = None
