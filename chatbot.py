import os
import json
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from ats import calculate_ats_score

from prompts import (
    build_summary_prompt,
    build_ats_prompt,
    build_skills_prompt,
    build_roles_prompt,
    build_interview_prompt,
    build_improvement_prompt,
    build_cert_prompt,
    build_project_prompt,
    build_experience_prompt,
    build_general_prompt,
    build_jd_prompt
)

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

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def clean_json_response(content: str):

    content = content.strip()

    if content.startswith("```json"):
        content = (
            content.replace("```json", "")
            .replace("```", "")
            .strip()
        )

    elif content.startswith("```"):
        content = (
            content.replace("```", "")
            .strip()
        )

    return content


def normalize_response(analysis):

    list_fields = [
        "skills",
        "missing_skills",
        "recommended_roles",
        "interview_questions",
        "resume_improvements",
        "certifications",
        "projects",
        "matching_skills",
        "strengths",
        "weaknesses",
        "suggestions",
        "ats_keywords"
    ]

    for field in list_fields:

        value = analysis.get(field)

        if value is None:

            analysis[field] = []

        elif isinstance(value, str):

            analysis[field] = [value]

        elif not isinstance(value, list):

            analysis[field] = [str(value)]

    return analysis


# ---------------------------------------------------------
# Resume Chat
# ---------------------------------------------------------

def ask_resume(
    question,
    vector_store,
    intent,
    chat_history
):

    if intent in ["experience", "general"]:
        docs = vector_store.similarity_search(
            question,
            k=15
        )
    else:
        docs = vector_store.similarity_search(
            question,
            k=10
        )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    history = "\n".join(
        f"{role}: {message}"
        for role, message in chat_history[-6:]
    )

    if intent == "summary":
        prompt = build_summary_prompt(context)
    elif intent == "ats":
        prompt = build_ats_prompt(context)
    elif intent == "skills":
        prompt = build_skills_prompt(context)
    elif intent == "roles":
        prompt = build_roles_prompt(context)
    elif intent == "interview":
        prompt = build_interview_prompt(context)
    elif intent == "improve":
        prompt = build_improvement_prompt(context)
    elif intent == "certifications":
        prompt = build_cert_prompt(context)
    elif intent == "projects":
        prompt = build_project_prompt(context)
    elif intent == "experience":
        prompt = build_experience_prompt(context)
    else:
        prompt = build_general_prompt(
            context,
            question,
            history
        )

    response = llm.invoke(prompt)

    content = clean_json_response(
        response.content
    )

    try:

        analysis = json.loads(content.strip())
        if intent == "general" and isinstance(analysis.get("answer"), str):
            analysis["answer"] = analysis["answer"].strip()

    except json.JSONDecodeError:

        if intent == "experience":

            analysis = {
                "experience": content
            }

        elif intent == "general":

            analysis = {
                "answer": content
            }

        else:

            analysis = {
                "answer":
                "⚠ Sorry, I couldn't analyze this request. Please try again."
            }

    analysis = normalize_response(
        analysis
    )

    score = analysis.get("match_score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0

    if score <= 1:
        score *= 100

    analysis["match_score"] = max(0, min(100, int(score)))

    analysis.setdefault(
        "match_score",
        0
    )

    if intent == "ats":
        analysis["ats_score"] = calculate_ats_score(
            context
        )

    return analysis, docs
# ---------------------------------------------------------
# Resume vs Job Description
# ---------------------------------------------------------

def compare_resume(vector_store, job_description):

    docs = vector_store.similarity_search(
        job_description,
        k=12
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = build_jd_prompt(
        context,
        job_description
    )

    response = llm.invoke(prompt)

    content = clean_json_response(
        response.content
    )

    try:
        analysis = json.loads(content.strip())

    except json.JSONDecodeError:

        analysis = {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "resume_improvements": [],
            "ats_keywords": []
        }

    score = analysis.get("match_score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        score = 0

    if score <= 1:
        score *= 100

    analysis["match_score"] = max(0, min(100, int(score)))

    analysis = normalize_response(
        analysis
    )

    return analysis