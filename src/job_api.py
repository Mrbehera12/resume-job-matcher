
import os

import requests
from dotenv import load_dotenv

from src.models import Job
from src.skill_extractor import extract_skills

load_dotenv()

BASE_URL = "https://api.adzuna.com/v1/api"


def search_adzuna_jobs(
    query: str,
    location: str | None = None,
    page: int = 1,
    results_per_page: int = 10,
) -> list[Job]:
    """Fetch Adzuna job listings and convert them into Job objects."""

    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise RuntimeError("Adzuna credentials are not configured.")

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if page < 1:
        raise ValueError("Page must be 1 or greater.")

    if not 1 <= results_per_page <= 50:
        raise ValueError("results_per_page must be between 1 and 50.")

    url = f"{BASE_URL}/jobs/in/search/{page}"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query.strip(),
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }

    if location:
        params["where"] = location

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Adzuna request timed out.") from exc

    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code
        raise RuntimeError(
            f"Adzuna returned HTTP {status}. "
            "Check credentials, access and API limits."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError("Could not connect to Adzuna.") from exc

    except ValueError as exc:
        raise RuntimeError("Adzuna returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise RuntimeError("Unexpected Adzuna response format.")

    records = data.get("results")

    if not isinstance(records, list):
        raise RuntimeError("Adzuna response has no valid results list.")

    jobs = []

    for record in records:
        if not isinstance(record, dict):
            continue

        job_id = record.get("id")
        title = record.get("title")
        description = record.get("description") or ""

        if not job_id or not title:
            continue

        company_data = record.get("company") or {}
        location_data = record.get("location") or {}

        company = (
            company_data.get("display_name")
            if isinstance(company_data, dict)
            else None
        )

        location_name = (
            location_data.get("display_name")
            if isinstance(location_data, dict)
            else None
        )

        job_text = f"{title} {description}"

        job = Job(
            job_id=str(job_id),
            title=title.strip(),
            company=company or "Not specified",
            description=description,
            skills=extract_skills(job_text),
            location=location_name or "Not specified",
            job_url=record.get("redirect_url"),
        )

        jobs.append(job)

    return jobs
