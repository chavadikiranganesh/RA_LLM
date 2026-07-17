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

groq_api_key = (
    st.secrets.get("GROQ_API_KEY")
    or os.getenv("GROQ_API_KEY")
)

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)


# ---------------------------------------------------------
# Helper Function
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


# ---------------------------------------------------------
# Resume Chat
# ---------------------------------------------------------

def ask_resume(
    question,
    vector_store,
    intent,
    chat_history
):

    # Retrieve relevant resume chunks

    docs = vector_store.similarity_search(
        question,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Conversation history

    history = "\n".join(
        f"{role}: {message}"
        for role, message in chat_history[-6:]
    )

    # ---------------- Prompt Routing ---------------- #

    if intent == "summary":

        prompt = build_summary_prompt(
            context
        )

    elif intent == "ats":

        prompt = build_ats_prompt(
            context
        )

    elif intent == "skills":

        prompt = build_skills_prompt(
            context
        )

    elif intent == "roles":

        prompt = build_roles_prompt(
            context
        )

    elif intent == "interview":

        prompt = build_interview_prompt(
            context
        )

    elif intent == "improve":

        prompt = build_improvement_prompt(
            context
        )

    elif intent == "certifications":

        prompt = build_cert_prompt(
            context
        )

    elif intent == "projects":

        prompt = build_project_prompt(
            context
        )

    elif intent == "experience":

        prompt = build_experience_prompt(
            context
        )

    else:

        prompt = build_general_prompt(
            context,
            question,
            history
        )

    # Invoke LLM

    response = llm.invoke(prompt)

    content = clean_json_response(
        response.content
    )

    try:

        analysis = json.loads(content)

    except Exception:

        analysis = {
            "answer": content
        }

    # ATS Score

    if intent == "ats":

        analysis["ats_score"] = calculate_ats_score(
            context
        )

    return analysis, docs
# ---------------------------------------------------------
# Resume vs Job Description
# ---------------------------------------------------------

def compare_resume(vector_store, job_description):

    # Retrieve the most relevant resume chunks
    docs = vector_store.similarity_search(
        job_description,
        k=5
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Build JD comparison prompt
    prompt = build_jd_prompt(
        context,
        job_description
    )

    # Call LLM
    response = llm.invoke(prompt)

    content = clean_json_response(
        response.content
    )

    try:

        analysis = json.loads(content)

    except Exception:

        analysis = {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "resume_improvements": []
        }

    # Ensure all keys exist

    analysis.setdefault("match_score", 0)
    analysis.setdefault("matching_skills", [])
    analysis.setdefault("missing_skills", [])
    analysis.setdefault("strengths", [])
    analysis.setdefault("weaknesses", [])
    analysis.setdefault("suggestions", [])
    analysis.setdefault("resume_improvements", [])

    return analysis