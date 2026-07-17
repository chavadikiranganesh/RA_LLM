# ---------------- SUMMARY ---------------- #

SUMMARY_PROMPT = """
You are an expert Technical Recruiter.

Using ONLY the uploaded resume, write a professional summary.

Return ONLY JSON.

{
    "summary":""
}

Resume:
{context}
"""

def build_summary_prompt(context):
    return SUMMARY_PROMPT.format(context=context)


# ---------------- ATS ---------------- #

ATS_PROMPT = """
You are an ATS evaluator.

Evaluate ONLY the uploaded resume.

Return ONLY JSON.

{
    "ats_score":0,
    "reason":""
}

Resume:
{context}
"""

def build_ats_prompt(context):
    return ATS_PROMPT.format(context=context)


# ---------------- SKILLS ---------------- #

SKILLS_PROMPT = """
You are a technical recruiter.

Identify the candidate's skills and missing skills.

Return ONLY JSON.

{
    "skills":[],
    "missing_skills":[]
}

Resume:
{context}
"""

def build_skills_prompt(context):
    return SKILLS_PROMPT.format(context=context)


# ---------------- ROLES ---------------- #

ROLE_PROMPT = """
You are a career advisor.

Recommend suitable job roles.

Return ONLY JSON.

{
    "recommended_roles":[]
}

Resume:
{context}
"""

def build_roles_prompt(context):
    return ROLE_PROMPT.format(context=context)


# ---------------- INTERVIEW ---------------- #

INTERVIEW_PROMPT = """
You are a senior interviewer.

Generate interview questions from the resume.

Return ONLY JSON.

{
    "interview_questions":[]
}

Resume:
{context}
"""

def build_interview_prompt(context):
    return INTERVIEW_PROMPT.format(context=context)


# ---------------- RESUME IMPROVEMENT ---------------- #

IMPROVEMENT_PROMPT = """
You are an ATS resume expert.

Improve the uploaded resume.

Return ONLY JSON.

{
    "resume_improvements":[]
}

Resume:
{context}
"""

def build_improvement_prompt(context):
    return IMPROVEMENT_PROMPT.format(context=context)


# ---------------- CERTIFICATIONS ---------------- #

CERT_PROMPT = """
Suggest certifications based on the uploaded resume.

Return ONLY JSON.

{
    "certifications":[]
}

Resume:
{context}
"""

def build_cert_prompt(context):
    return CERT_PROMPT.format(context=context)


# ---------------- PROJECTS ---------------- #

PROJECT_PROMPT = """
Analyze the projects in the resume.

Return ONLY JSON.

{
    "projects":[]
}

Resume:
{context}
"""

def build_project_prompt(context):
    return PROJECT_PROMPT.format(context=context)


# ---------------- EXPERIENCE ---------------- #

EXPERIENCE_PROMPT = """
Analyze the work experience.

Return ONLY JSON.

{
    "experience":""
}

Resume:
{context}
"""

def build_experience_prompt(context):
    return EXPERIENCE_PROMPT.format(context=context)


# ---------------- GENERAL CHAT ---------------- #

GENERAL_PROMPT = """
You are an AI Resume Assistant.

You are given:

1. Conversation History
2. Resume Context
3. User Question

Conversation History:
{history}

Resume Context:
{context}

Current Question:
{question}

Instructions:

- Use BOTH the conversation history and the resume context.
- Answer naturally like ChatGPT.
- If the question is a follow-up, use the previous conversation.
- Do NOT invent information.
- If the answer is not present in the resume, politely say so.
- Keep the response concise and professional.
"""

def build_general_prompt(context, question, history):

    return GENERAL_PROMPT.format(
        context=context,
        question=question,
        history=history
    )