import re


def calculate_ats_score(text):

    score = 0

    text = text.lower()

    # Education
    if "bachelor" in text or "b.tech" in text:
        score += 15

    # Experience
    if "intern" in text or "experience" in text:
        score += 15

    # Projects
    if "project" in text:
        score += 15

    # Skills
    skills = [
        "python",
        "sql",
        "machine learning",
        "pandas",
        "numpy",
        "tableau",
        "power bi",
        "git",
        "github",
        "flask",
        "react",
        "mongodb",
        "mysql"
    ]

    skill_count = 0

    for skill in skills:
        if skill in text:
            skill_count += 1

    score += min(skill_count * 3, 30)

    # Certifications
    if "certification" in text or "oracle" in text:
        score += 10

    # Contact Information
    if re.search(r"\S+@\S+", text):
        score += 5

    return min(score, 100)