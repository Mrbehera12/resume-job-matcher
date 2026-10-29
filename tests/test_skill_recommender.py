import pytest

from src.skill_recommender import recommend_skills


def test_recommends_most_requested_missing_skills_first():
    results = [
        {"title": "Python Developer", "missing_skills": ["Docker", "SQL"],
         "total_detected_skills": 4, "skill_data_status": "skills_detected"},
        {"title": "Backend Developer", "missing_skills": ["Docker", "AWS"],
         "total_detected_skills": 3, "skill_data_status": "skills_detected"},
        {"title": "Data Analyst", "missing_skills": ["SQL", "Excel"],
         "total_detected_skills": 3, "skill_data_status": "skills_detected"},
    ]

    recommendations = recommend_skills(results)

    assert [x["skill"] for x in recommendations] == [
        "Docker", "SQL", "AWS", "Excel"
    ]
    assert recommendations[0]["jobs_requesting"] == 2
    assert recommendations[0]["job_demand_percent"] == 66.67


def test_skips_jobs_without_detected_skill_data():
    results = [
        {"title": "Unknown role", "missing_skills": ["Docker"],
         "total_detected_skills": 0, "skill_data_status": "no_detected_skills"},
        {"title": "Backend Developer", "missing_skills": ["SQL"],
         "total_detected_skills": 2, "skill_data_status": "skills_detected"},
    ]

    recommendations = recommend_skills(results)

    assert len(recommendations) == 1
    assert recommendations[0]["skill"] == "SQL"
    assert recommendations[0]["job_demand_percent"] == 100.0


def test_deduplicates_same_skill_within_a_job_case_insensitively():
    results = [
        {"title": "Backend Developer",
         "missing_skills": ["Docker", "docker", " Docker "],
         "total_detected_skills": 3, "skill_data_status": "skills_detected"}
    ]

    recommendations = recommend_skills(results)

    assert len(recommendations) == 1
    assert recommendations[0]["jobs_requesting"] == 1


def test_top_n_limits_results_and_ties_sort_alphabetically():
    results = [
        {"title": "Role", "missing_skills": ["Docker", "SQL", "AWS"],
         "total_detected_skills": 3, "skill_data_status": "skills_detected"}
    ]

    recommendations = recommend_skills(results, top_n=2)

    assert len(recommendations) == 2
    assert [x["skill"] for x in recommendations] == ["AWS", "Docker"]


def test_rejects_invalid_top_n():
    with pytest.raises(ValueError, match="top_n must be at least 1"):
        recommend_skills([], top_n=0)


def test_empty_input_returns_empty_list():
    assert recommend_skills([]) == []
