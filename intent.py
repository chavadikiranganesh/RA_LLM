import os
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ---------------------------------------------------------
# Load Environment
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# Load Groq API Key
# ---------------------------------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to .env for local development "
        "or secrets.toml for Streamlit Cloud."
    )

# ---------------------------------------------------------
# Initialize LLM
# ---------------------------------------------------------

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

PROMPT = """
You are an intent classifier for an AI Resume Assistant.

Classify the user's question into EXACTLY ONE of these categories:

- summary
- ats
- skills
- roles
- interview
- improve
- certifications
- projects
- experience
- general

Intent definitions:

summary:
- Resume summary
- Profile summary
- About the candidate

ats:
- ATS score
- ATS evaluation
- Resume score

skills:
- Explicit requests to list skills
- Technical skills
- Soft skills
- Missing skills

roles:
- Suitable job roles
- Career suggestions
- Recommended positions

interview:
- Interview questions
- Mock interview

improve:
- Resume improvement
- Resume suggestions
- Resume feedback

certifications:
- Certifications
- Courses
- Licenses

projects:
- List projects
- Explain projects
- Project details

experience:
- Internship
- Work experience
- Professional experience

general:
- Any other question about the resume.
- Questions like:
  • Which databases do I know?
  • Which ML algorithms have I used?
  • Which programming languages do I know?
  • Which frameworks have I used?
  • What technologies did I use there?
  • Follow-up questions referring to previous answers.
  • Any question asking for specific information from the resume.

Rules:
- Return ONLY one category.
- Do NOT explain.
- Return ONLY the category name.
- If unsure, return "general".

Question:
{question}
"""


def detect_intent(question):

    try:
        response = llm.invoke(
            PROMPT.format(question=question)
        )

        intent = response.content.strip().lower()

        valid_intents = {
            "summary",
            "ats",
            "skills",
            "roles",
            "interview",
            "improve",
            "certifications",
            "projects",
            "experience",
            "general"
        }

        if intent not in valid_intents:
            return "general"

        return intent

    except Exception:
        return "general"