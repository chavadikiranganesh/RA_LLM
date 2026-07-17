import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

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

Rules:
- Return ONLY one category.
- Do not explain your answer.
- Do not return punctuation or extra text.
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