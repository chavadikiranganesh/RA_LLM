import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from prompts import build_prompt, build_jd_prompt
from ats import calculate_ats_score

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)


def ask_resume(question, vector_store):
    """
    Ask questions about the uploaded resume.
    """

    # Retrieve relevant chunks
    docs = vector_store.similarity_search(
        question,
        k=3
    )

    # Combine retrieved chunks
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Build prompt
    prompt = build_prompt(
        context=context,
        question=question
    )

    # Call LLM
    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        analysis = json.loads(content)

        # Replace AI ATS score with your ATS algorithm
        analysis["ats_score"] = calculate_ats_score(context)

    except json.JSONDecodeError:

        analysis = {
            "summary": content,
            "ats_score": calculate_ats_score(context),
            "strengths": [],
            "weaknesses": [],
            "recommended_roles": [],
            "missing_skills": [],
            "interview_questions": []
        }

    return analysis, docs


def compare_resume(vector_store, job_description):
    """
    Compare uploaded resume with Job Description.
    """

    # Retrieve resume sections relevant to the JD
    docs = vector_store.similarity_search(
        job_description,
        k=5
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # Build JD prompt
    prompt = build_jd_prompt(
        context=context,
        job_description=job_description
    )

    # Call LLM
    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        analysis = json.loads(content)

    except json.JSONDecodeError:

        analysis = {
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "suggestions": []
        }

    return analysis