# ---------------- SUMMARY ---------------- #

SUMMARY_PROMPT = """
You are an expert Technical Recruiter.

Using ONLY the uploaded resume, write a professional summary.

Return ONLY JSON.

{{
    "summary":""
}}

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

{{
    "ats_score":0,
    "reason":""
}}

Resume:
{context}
"""

def build_ats_prompt(context):
    return ATS_PROMPT.format(context=context)

SKILLS_PROMPT = """
You are an expert technical recruiter.

Extract every technical skill from the resume.

Also identify important missing skills for modern software engineering roles.

Return ONLY valid JSON.

{
    "skills":[
        "Python"
    ],
    "missing_skills":[
        "Docker"
    ]
}

Resume:
{context}
"""


# ---------------- ROLES ---------------- #

ROLE_PROMPT = """
You are a career advisor.

Recommend suitable job roles.

Return ONLY JSON.

{{
    "recommended_roles":[]
}}

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

{{
    "interview_questions":[]
}}

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

{{
    "resume_improvements":[]
}}

Resume:
{context}
"""

def build_improvement_prompt(context):
    return IMPROVEMENT_PROMPT.format(context=context)


# ---------------- CERTIFICATIONS ---------------- #

CERT_PROMPT = """
Suggest certifications based on the uploaded resume.

Return ONLY JSON.

{{
    "certifications":[]
}}

Resume:
{context}
"""

def build_cert_prompt(context):
    return CERT_PROMPT.format(context=context)

PROJECT_PROMPT = """
You are an expert technical recruiter.

Extract ALL projects mentioned in the resume.

For each project include:
- Project Name
- One-line description
- Technologies used (if available)

Return ONLY valid JSON.

{
    "projects":[
        "Project Name - Description (Technologies)"
    ]
}

Resume:
{context}
"""

# ---------------- EXPERIENCE ---------------- #

EXPERIENCE_PROMPT = """
Analyze the work experience.

Return ONLY JSON.

{{
    "experience":""
}}

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

Return ONLY JSON.

{{
    "answer":""
}}
"""

def build_general_prompt(context, question, history):
    return GENERAL_PROMPT.format(
        context=context,
        question=question,
        history=history
    )


# ---------------- JD MATCHING ---------------- #

JD_PROMPT = """
You are an ATS Resume Evaluator.

Compare the uploaded resume with the Job Description.

Return ONLY JSON.

{{
    "match_score":0,
    "matching_skills":[],
    "missing_skills":[],
    "strengths":[],
    "weaknesses":[],
    "suggestions":[],
    "resume_improvements":[]
}}

Resume:
{context}

Job Description:
{job_description}
"""

def build_jd_prompt(context, job_description):
    return JD_PROMPT.format(
        context=context,
        job_description=job_description
    )