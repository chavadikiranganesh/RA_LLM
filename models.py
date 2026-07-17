from pydantic import BaseModel
from typing import List


class ResumeAnalysis(BaseModel):

    summary: str

    ats_score: int

    strengths: List[str]

    weaknesses: List[str]

    recommended_roles: List[str]

    missing_skills: List[str]

    interview_questions: List[str]