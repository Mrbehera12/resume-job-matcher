
from src.skill_extractor import extract_skills, normalize_skill


def test_extract_known_skills():
    text = "I use Python, PostgreSQL, Docker and AWS."

    skills = extract_skills(text)

    assert skills == [
        "Python",
        "PostgreSQL",
        "AWS",
        "Docker",
    ]


def test_skill_extraction_is_case_insensitive():
    skills = extract_skills("python PYTHON Sql")

    assert skills == ["Python", "SQL"]


def test_unknown_skill_is_not_returned():
    skills = extract_skills("I work with an unknown tool.")

    assert skills == []


def test_skill_is_not_detected_inside_another_word():
    skills = extract_skills("I enjoy painting.")

    assert "Git" not in skills


def test_skill_aliases_return_canonical_names():
    skills = extract_skills(
        "Postgres, PostgreSQL, Amazon Web Services, node js, "
        "nodejs, and scikit learn."
    )

    assert skills == [
        "PostgreSQL",
        "AWS",
        "Node.js",
        "scikit-learn",
    ]


def test_normalize_skill_maps_aliases_case_insensitively():
    assert normalize_skill("  POSTGRES  ") == "PostgreSQL"


def test_normalize_skill_preserves_unknown_skill_text():
    assert normalize_skill("  Custom Tool  ") == "Custom Tool"


def test_skill_aliases_normalize():
    assert normalize_skill("Postgres") == "PostgreSQL"
    assert normalize_skill("POSTGRESQL") == "PostgreSQL"
    assert normalize_skill("Amazon Web Services") == "AWS"
    assert normalize_skill("Node JS") == "Node.js"


def test_unknown_skill_keeps_original_name():
    assert normalize_skill("Python") == "Python"
