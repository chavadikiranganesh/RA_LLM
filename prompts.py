# ==========================================================
# SUMMARY
# ==========================================================

SUMMARY_PROMPT = """
You are an expert Technical Recruiter.

Analyze ONLY the uploaded resume.

Write a professional summary (80–120 words) highlighting:

- Education
- Technical Skills
- Internship / Experience
- Major Projects
- Career Objective

Rules:
- Use ONLY information from the resume.
- Do NOT invent information.
- Keep the tone professional.
- Return ONLY valid JSON.

{{
    "summary":""
}}

Resume:
{context}
"""

def build_summary_prompt(context):
    return SUMMARY_PROMPT.format(context=context)


# ==========================================================
# ATS
# ==========================================================

ATS_PROMPT = """
You are an ATS Resume Evaluator.

Evaluate ONLY the uploaded resume.

Consider:

- Resume Structure
- ATS Keywords
- Technical Skills
- Experience
- Projects
- Certifications

Return ONLY valid JSON.

{{
    "ats_score":0,
    "reason":"",
    "strengths":[],
    "weaknesses":[]
}}

Rules:

- ATS score must be an INTEGER between 0 and 100.
- Do NOT return decimals.
- Return ONLY valid JSON.

Resume:
{context}
"""

def build_ats_prompt(context):
    return ATS_PROMPT.format(context=context)


# ==========================================================
# SKILLS
# ==========================================================

SKILLS_PROMPT = """
You are an expert Technical Recruiter.

Extract ALL technical skills from the resume.

Categorize them into:

- Programming Languages
- Frameworks
- Databases
- Tools
- Cloud Technologies

Also identify important missing skills for modern software engineering roles.

Return ONLY valid JSON.

{{
    "skills":[
        "Python",
        "Pandas",
        "Scikit-learn",
        "SQL",
        "Git"
    ],
    "missing_skills":[
        "Docker",
        "Kubernetes",
        "CI/CD"
    ]
}}

Rules:

- Do NOT invent skills.
- Extract ONLY from the resume.
- Return ONLY JSON.

Resume:
{context}
"""

def build_skills_prompt(context):
    return SKILLS_PROMPT.format(context=context)


# ==========================================================
# RECOMMENDED ROLES
# ==========================================================

ROLE_PROMPT = """
You are a Senior Technical Recruiter.

Analyze ONLY the uploaded resume.

Recommend the TOP 5 most suitable job roles based ONLY on:

- Skills
- Projects
- Internship
- Experience
- Technologies
- Education
- Certifications

Rules:

- Recommend ONLY realistic roles.
- If the candidate is a fresher, recommend entry-level roles.
- Do NOT recommend unrelated positions.
- Return ONLY valid JSON.

Example:

{{
    "recommended_roles":[
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Python Developer",
        "Data Analyst"
    ]
}}

Resume:
{context}
"""

def build_roles_prompt(context):
    return ROLE_PROMPT.format(context=context)


# ==========================================================
# INTERVIEW QUESTIONS
# ==========================================================

INTERVIEW_PROMPT = """
You are a Senior Technical Interviewer.

Generate interview questions based ONLY on the uploaded resume.

Generate:

- 5 Technical Questions
- 3 Project-based Questions
- 2 HR Questions

Return ONLY valid JSON.

{{
    "interview_questions":[
        "Question 1",
        "Question 2"
    ]
}}

Rules:

- Questions must match the candidate's skills.
- Include project-based questions.
- Return ONLY JSON.

Resume:
{context}
"""

def build_interview_prompt(context):
    return INTERVIEW_PROMPT.format(context=context)


# ==========================================================
# RESUME IMPROVEMENTS
# ==========================================================

IMPROVEMENT_PROMPT = """
You are an ATS Resume Expert.

Analyze ONLY the uploaded resume.

Suggest practical improvements.

Focus on:

- ATS Optimization
- Technical Skills
- Resume Structure
- Projects
- Experience
- Keywords
- Achievements

Return ONLY valid JSON.

{{
    "resume_improvements":[
        "Add measurable achievements.",
        "Improve ATS keywords.",
        "Include GitHub profile.",
        "Quantify internship impact."
    ]
}}

Rules:

- Return ONLY a list of strings.
- Do NOT return nested JSON.
- Do NOT use markdown.
- Return ONLY valid JSON.

Resume:
{context}
"""

def build_improvement_prompt(context):
    return IMPROVEMENT_PROMPT.format(context=context)


# ==========================================================
# CERTIFICATIONS
# ==========================================================

CERT_PROMPT = """
You are a Senior Technical Recruiter and Career Advisor.

Analyze ONLY the uploaded resume.

Recommend the top 5 certifications that would strengthen the candidate's profile.

Base your recommendations on:
- Technical Skills
- Programming Languages
- Frameworks
- Cloud Technologies
- Tools
- Projects
- Experience
- Career Domain

Rules:
- Recommend certifications relevant to the candidate's profile.
- Do NOT recommend certifications already present in the resume.
- Do NOT recommend companies, learning platforms, institutes, or training providers.
- Return ONLY official certification names.
- Return at most 5 certifications.
- Adapt recommendations to the candidate's skills and career path.

Return ONLY valid JSON.

{{
    "certifications":[]
}}

Resume:
{context}
"""
def build_cert_prompt(context):
    return CERT_PROMPT.format(context=context)


# ==========================================================
# PROJECTS
# ==========================================================

PROJECT_PROMPT = """
You are an expert Technical Recruiter.

Extract ALL projects from the uploaded resume.

For EACH project provide:

- Project Name
- One-line Description
- Technologies Used

Return ONLY valid JSON.

{{
    "projects":[
        {{
            "project_name":"",
            "description":"",
            "technologies":""
        }}
    ]
}}

Rules:

- Extract ONLY projects from the resume.
- Do NOT invent projects.
- Technologies should be comma separated.
- Return ONLY JSON.

Resume:
{context}
"""

def build_project_prompt(context):
    return PROJECT_PROMPT.format(context=context)


# ==========================================================
# EXPERIENCE
# ==========================================================

EXPERIENCE_PROMPT = """
You are an expert Resume Reviewer.

Using ONLY the uploaded resume, write a professional experience summary.

Include:

- Internship / Company Name
- Duration
- Responsibilities
- Technologies Used
- Major Achievements
- Mention important projects completed during the internship.

Rules:

- Use ONLY resume information.
- Do NOT invent information.
- Keep the response within 120 words.
- Return ONLY plain English.
- Do NOT return JSON.
- Do NOT use markdown.

Resume:
{context}
"""

def build_experience_prompt(context):
    return EXPERIENCE_PROMPT.format(context=context)


# ==========================================================
# GENERAL CHAT
# ==========================================================

GENERAL_PROMPT = """
You are an AI Resume Assistant.

You are given:

1. Conversation History
2. Resume Context
3. Current User Question

Conversation History:
{history}

Resume Context:
{context}

Current Question:
{question}

Instructions:

- Answer naturally like ChatGPT.
- Use BOTH conversation history and resume context.
- Answer ONLY from the resume.
- Never invent information.
- If the answer isn't available in the resume, politely say so.
- Keep answers concise and professional.
- Understand follow-up questions.

Return ONLY valid JSON.

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


# ==========================================================
# JOB DESCRIPTION MATCHING
# ==========================================================

JD_PROMPT = """
You are an expert ATS (Applicant Tracking System) Resume Evaluator.

Compare the uploaded resume against the Job Description.

Evaluate the resume based on:

1. Technical Skills
2. Programming Languages
3. Frameworks & Libraries
4. Databases
5. Cloud Technologies
6. Tools & Platforms
7. Certifications
8. Projects
9. Experience
10. Responsibilities
11. ATS Keyword Coverage

Return ONLY valid JSON.

{{
    "match_score": 0,

    "matching_skills": [],

    "missing_skills": [],

    "strengths": [],

    "weaknesses": [],

    "suggestions": [],

    "resume_improvements": [],

    "ats_keywords": [
        {{
            "keyword": "",
            "status": "Matched",
            "importance": "High"
        }}
    ]
}}

Rules:

- match_score MUST be an INTEGER between 0 and 100.
- Do NOT return decimals.
- Do NOT invent any information.
- Compare ONLY using the resume and job description.
- Include ONLY important ATS keywords from the Job Description.
- Mark each keyword as either "Matched" or "Missing".
- Importance must be one of:
    - High
    - Medium
    - Low
- High importance keywords are core technical skills required for the role.
- Medium importance keywords are supporting technologies.
- Low importance keywords are optional or preferred skills.
- Return at least 10 ATS keywords whenever possible.
- Return ONLY valid JSON.
- Do NOT include explanations outside JSON.

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