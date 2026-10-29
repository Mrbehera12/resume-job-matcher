
import re

SKILL_VOCABULARY = [
    # Programming languages
    "C",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "Python",
    "Swift",
    "Kotlin",
    "SQL",
    "PL/SQL",

    # Web development
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "Django",
    "Flask",
    "FastAPI",
    "Spring Boot",
    "REST API",
    "GraphQL",

    # Databases
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "SQLite",
    "Oracle",

    # Cloud and DevOps
    "AWS",
    "Azure",
    "Google Cloud",
    "Docker",
    "Kubernetes",
    "Linux",
    "Git",
    "GitHub",
    "Jenkins",
    "CI/CD",

    # Data and AI
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Data Visualization",
    "Power BI",
    "Tableau",
    "Excel",
    "Hadoop",
    "Apache Spark",
]

SKILL_ALIASES = {
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "amazon web services": "AWS",
    "node js": "Node.js",
    "nodejs": "Node.js",
    "scikit learn": "scikit-learn",
}


def normalize_skill(skill: str) -> str:
    """Convert known skill names and aliases to canonical names."""
    cleaned = skill.strip()
    return SKILL_ALIASES.get(
        cleaned.casefold(),
        cleaned,
    )



def extract_skills(text: str) -> list[str]:
    """Find known skills and normalize their names."""

    found_skills = []
    seen = set()

    # Search both canonical names and known aliases.
    candidates = list(SKILL_VOCABULARY) + list(SKILL_ALIASES)

    for skill in candidates:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            canonical = normalize_skill(skill)
            key = canonical.casefold()

            if key not in seen:
                seen.add(key)
                found_skills.append(canonical)

    return found_skills
