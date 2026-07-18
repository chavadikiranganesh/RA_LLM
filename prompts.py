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

{{
    "skills":[
        "Python"
    ],
    "missing_skills":[
        "Docker"
    ]
}}

Resume:
{context}
"""

def build_skills_prompt(context):
    return SKILLS_PROMPT.format(context=context)
# ---------------- ROLES ---------------- #

ROLE_PROMPT = """
You are an expert Technical Recruiter.

Analyze ONLY the uploaded resume.

Recommend the TOP 5 most suitable job roles based ONLY on:

- Skills
- Projects
- Internship/Experience
- Technologies
- Education
- Certifications

Rules:
- Recommend ONLY roles that match the resume.
- Do NOT recommend unrelated roles.
- If the resume is for a fresher, recommend entry-level roles.
- Return ONLY valid JSON.
- Do NOT include explanations.

Return ONLY:

{{
    "recommended_roles": [
        "Role 1",
        "Role 2",
        "Role 3",
        "Role 4",
        "Role 5"
    ]
}}

Resume:
{context}
"""

def build_roles_prompt(context):
    try:
        return ROLE_PROMPT.format(context=context)
    except Exception as e:
        print("FORMAT ERROR:", repr(e))
        raise


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

Analyze the uploaded resume and provide practical improvements.

Return ONLY valid JSON.

{{
    "resume_improvements": [
        "Improve the professional summary.",
        "Add measurable achievements.",
        "Include more ATS keywords."
    ]
}}

Rules:
- Return ONLY valid JSON.
- resume_improvements MUST be a list of strings.
- Do NOT return dictionaries.
- Do NOT return nested JSON.
- Do NOT include markdown.

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

Do NOT skip any project.

Return ONLY valid JSON.

{{
    "projects":[
        "Project Name - Description (Technologies)"
    ]
}}

Resume:
{context}
"""

def build_project_prompt(context):
    return PROJECT_PROMPT.format(context=context)
# ---------------- EXPERIENCE ---------------- #
EXPERIENCE_PROMPT = """
You are an expert resume reviewer.

Using ONLY the uploaded resume, write a professional experience summary.

Include:
- Internship/company name
- Duration
- Main responsibilities
- Key technologies used
- Mention ALL major projects found in the resume with one short sentence each.

Return ONLY plain English.
Do NOT return JSON.
Do NOT use markdown.
Limit the response to about 120 words.

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