from report_generator import create_pdf
from styles import load_css

import streamlit as st

from utils import process_pdf
from chatbot import ask_resume, compare_resume
from intent import detect_intent


def format_response(value):
    """
    Convert any response into a displayable string.
    """

    if value is None:
        return ""

    if isinstance(value, list):
        return "\n".join(str(item) for item in value)

    if isinstance(value, dict):
        return "\n".join(
            f"{k}: {v}" for k, v in value.items()
        )

    return str(value)


def display_project(project):
    """
    Display a project as a styled card with technology chips.
    """

    technologies = project.get("technologies", "")

    if isinstance(technologies, str):
        tech_list = [
            t.strip()
            for t in technologies.split(",")
            if t.strip()
        ]
    else:
        tech_list = technologies

    tech_html = ""

    for tech in tech_list:
        tech_html += f'<span class="tech-chip">{tech}</span>'

    st.markdown(
        f"""
        <div class="project-card">

            <div class="project-title">
                📂 {project.get("project_name", "Project")}
            </div>

            <div class="project-desc">
                {project.get("description", "No description")}
            </div>

            {tech_html}

        </div>
        """,
        unsafe_allow_html=True
    )


def display_chips(items):
    """
    Display items as styled skill chips using CSS classes.
    """

    if not items:
        st.info("No items found.")
        return

    html = ""

    for item in items:
        html += f'<span class="skill-chip">{item}</span>'

    st.markdown(html, unsafe_allow_html=True)


# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="LLM-Powered Resume Analyzer using RAG",
    page_icon="🤖",
    layout="wide"
)


# ---------------- Custom CSS ---------------- #
# ---------------- Custom CSS ---------------- #

st.markdown(load_css(), unsafe_allow_html=True)

# ==========================================================
# Hero Section
# ==========================================================

st.markdown(
    """
    <div class="hero">

        <div class="title">
            🤖 AI Resume Analyzer
        </div>

        <div class="subtitle">
            Powered by Llama 3.3 • LangChain • FAISS • HuggingFace
        </div>

        <div class="hero-text">
            Upload your resume and receive intelligent career insights,
            ATS evaluation, resume improvements, interview preparation,
            AI resume chat, and Job Description matching using
            Retrieval-Augmented Generation (RAG).
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# Feature Cards
# ==========================================================

st.markdown(
"""
<div class="feature-grid">

<div class="feature-card">
<div class="feature-icon">📄</div>
<div class="feature-title">Resume Summary</div>
<div class="feature-text">
Generate an AI-powered summary of your resume instantly.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">🎯</div>
<div class="feature-title">ATS Score</div>
<div class="feature-text">
Evaluate resume quality and ATS compatibility.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">💼</div>
<div class="feature-title">JD Matching</div>
<div class="feature-text">
Compare your resume against any Job Description.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">🤖</div>
<div class="feature-title">AI Resume Chat</div>
<div class="feature-text">
Ask anything about your resume using RAG.
</div>
</div>

</div>
""",
unsafe_allow_html=True
)
# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------- Sidebar ---------------- #
with st.sidebar:

    st.markdown("## 📂 Resume")

    st.caption("Upload your resume to unlock AI analysis.")

    uploaded_file = st.file_uploader(
        "Choose a PDF Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("📄 Reading Resume..."):
            st.session_state.vector_store = process_pdf(uploaded_file)

        st.session_state.messages = []
        st.session_state.chat_history = []

        st.success("✅ Resume uploaded successfully!")

    st.divider()

    st.markdown("## 💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    st.divider()

    st.markdown("## 💡 Quick Questions")

    st.markdown(
    """
- 📄 Summarize my resume
- ⭐ ATS Score
- 💻 Technical Skills
- 💼 Recommended Roles
- 🎤 Interview Questions
- 📂 Explain my projects
- 📚 Certifications
- 🎯 Resume vs Job Description
"""
    )

    st.divider()

    st.markdown("### ⚡ Powered By")

    st.markdown("""
🤖 Groq

🦜 LangChain

📚 HuggingFace

⚡ FAISS
""")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.chat_history = []

        st.rerun()
# ---------------- Welcome ---------------- #

st.markdown("""

# 👋 Welcome

Upload your resume to get

✅ AI Resume Summary

✅ ATS Score

✅ Technical Skills

✅ Resume Improvements

✅ Interview Questions

✅ AI Resume Chat

✅ Resume vs Job Description Matching

""")


# ---------------- Chat History ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- Chat ---------------- #

question = st.chat_input(
    "💬 Ask about skills, ATS, projects, experience or interview preparation..."
)

if question:

    if st.session_state.vector_store is None:

        st.warning("⚠ Please upload a resume first.")

    else:

        # Detect intent
        intent = detect_intent(question)
        # st.write("Detected Intent:", intent)

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Get AI response
        with st.spinner(
            "🤖 Reading Resume • Retrieving Knowledge • Generating AI Response..."
        ):

            analysis, docs = ask_resume(
                question,
                st.session_state.vector_store,
                intent,
                st.session_state.chat_history
            )

        with st.chat_message("assistant"):

            if "answer" in analysis and intent != "general":
                assistant_reply = analysis["answer"]
                st.warning(assistant_reply)

            # ---------------- SUMMARY ---------------- #

            if intent == "summary":

                assistant_reply = analysis.get("summary", "")

                with st.container(border=True):
                    st.subheader("📄 Resume Summary")
                    st.write(assistant_reply)

            # ---------------- ATS ---------------- #

            elif intent == "ats":

                score = analysis.get("ats_score", 0)

                assistant_reply = f"ATS Score : {score}/100"

                with st.container(border=True):

                    st.subheader("🎯 ATS Score")

                    st.metric(
                        "Overall Score",
                        f"{score}/100"
                    )

                    st.progress(score / 100)

                    st.write(
                        analysis.get("reason", "")
                    )

            # ---------------- ROLES ---------------- #

            elif intent == "roles":

                roles = analysis.get("recommended_roles", [])

                if isinstance(roles, list):
                    assistant_reply = format_response(roles)

                elif isinstance(roles, str):
                    assistant_reply = roles

                elif isinstance(roles, dict):
                    assistant_reply = format_response(roles)

                else:
                    assistant_reply = str(roles)

                with st.container(border=True):

                    st.subheader("💼 Recommended Roles")

                    if isinstance(roles, list):
                        if roles:
                            for role in roles:
                                st.success(role)
                        else:
                            st.info("No suitable roles found.")

                    elif isinstance(roles, str):
                        st.success(roles)

                    elif isinstance(roles, dict):
                        for k, v in roles.items():
                            st.success(f"{k}: {v}")

                    else:
                        st.success(str(roles))

            # ---------------- SKILLS ---------------- #

            elif intent == "skills":

                skills = analysis.get("skills", [])
                missing = analysis.get("missing_skills", [])

                assistant_reply = format_response(skills)

                with st.container(border=True):

                    st.subheader("💻 Skills Analysis")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("✅ Skills")

                        if isinstance(skills, list):
                            display_chips(skills)
                        else:
                            st.success(format_response(skills))

                    with col2:

                        st.subheader("⚠ Missing Skills")

                        if isinstance(missing, list):
                            display_chips(missing)
                        else:
                            st.warning(format_response(missing))

            # ---------------- INTERVIEW ---------------- #

            elif intent == "interview":

                questions = analysis.get(
                    "interview_questions",
                    []
                )

                assistant_reply = format_response(questions)

                with st.container(border=True):

                    st.subheader("🎤 Interview Questions")

                    if isinstance(questions, list):
                        if questions:
                            for q in questions:
                                st.info(q)
                        else:
                            st.info("No interview questions generated.")
                    else:
                        st.info(format_response(questions))

            # ---------------- IMPROVE ---------------- #

            elif intent == "improve":

                improvements = analysis.get("resume_improvements", [])

                assistant_reply = format_response(improvements)

                with st.container(border=True):

                    st.subheader("📝 Resume Improvements")

                    if isinstance(improvements, list):
                        if improvements:
                            for tip in improvements:
                                st.success(tip)
                        else:
                            st.info("No resume improvements found.")

                    elif isinstance(improvements, str):
                        st.success(improvements)

                    elif isinstance(improvements, dict):
                        for key, value in improvements.items():
                            st.success(f"{key}: {value}")

                    else:
                        st.success(str(improvements))

            # ---------------- CERTIFICATIONS ---------------- #

            elif intent == "certifications":

                certs = analysis.get(
                    "certifications",
                    []
                )

                assistant_reply = format_response(certs)

                with st.container(border=True):

                    st.subheader("📚 Recommended Certifications")

                    if isinstance(certs, list):
                        if certs:
                            for cert in certs:
                                st.info(cert)
                        else:
                            st.info("No certifications suggested.")

                    else:
                        st.info(format_response(certs))
            # ---------------- PROJECTS ---------------- #

            elif intent == "projects":

                projects = analysis.get("projects", [])

                if isinstance(projects, list):
                    assistant_reply = format_response(projects)

                elif isinstance(projects, str):
                    assistant_reply = projects

                elif isinstance(projects, dict):
                    assistant_reply = format_response(projects)

                else:
                    assistant_reply = str(projects)

                with st.container(border=True):

                    st.subheader("📂 Projects")

                    if isinstance(projects, list):

                        if projects:

                            for project in projects:

                                if isinstance(project, dict):

                                    display_project(project)

                                else:

                                    st.success(project)

                        else:

                            st.info("No projects found.")

                    elif isinstance(projects, dict):

                        st.success(f"📂 {projects.get('Project Name','Project')}")

                        st.write(
                            f"**Description:** {projects.get('One-line description','Not available')}"
                        )

                        st.caption(
                            f"Technologies: {projects.get('Technologies used','Not available')}"
                        )

                    else:

                        st.success(format_response(projects))


            # ---------------- EXPERIENCE ---------------- #

            elif intent == "experience":

                assistant_reply = analysis.get(
                    "experience",
                    ""
                )

                with st.container(border=True):

                    st.subheader("💼 Experience")

                    st.write(assistant_reply)

            # ---------------- GENERAL ---------------- #

            else:

                assistant_reply = analysis.get(
                    "answer",
                    "No response generated."
                )

                st.write(assistant_reply)

            st.divider()

            pdf_file = create_pdf(analysis)
            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📥 Download AI Resume Report",
                    data=file,
                    file_name="Resume_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            st.divider()

            with st.expander("🔍 Retrieved Resume Context (RAG)", expanded=False):

                for i, doc in enumerate(
                    docs,
                    start=1
                ):

                    st.markdown(f"### Chunk {i}")
                    st.write(doc.page_content)
                    st.divider()

                # Save messages

            st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

        # Save conversation memory

            st.session_state.chat_history.append(
            (
                "Human",
                question
            )
        )

            st.session_state.chat_history.append(
            (
                "AI",
                assistant_reply
            )
        )

# ==========================================================
# Resume vs Job Description
# ==========================================================

st.divider()

st.header("🎯 Resume vs Job Description Matching")
st.caption("Compare your resume with any Job Description using AI.")

if st.button(
    "🚀 Compare Resume with Job Description",
    use_container_width=True
):

    if st.session_state.vector_store is None:

        st.warning("Please upload a resume.")

    elif job_description.strip() == "":

        st.warning("Please enter a Job Description.")

    else:

        with st.spinner(
            "🔍 Reading Resume • Comparing Skills • Calculating Match Score..."
        ):

            jd_analysis = compare_resume(
                st.session_state.vector_store,
                job_description
            )

        st.success("Comparison Complete!")

        with st.container(border=True):

            st.subheader("🎯 Overall Match Score")

            st.metric(
                "Resume Match",
                f"{jd_analysis['match_score']}%"
            )

            st.progress(
                jd_analysis["match_score"] / 100
            )

        st.subheader("✅ Matching Skills")
        matching = jd_analysis.get("matching_skills", [])

        if matching:
            display_chips(weaknesses)
        else:
            st.info("No matching skills found.")

        st.subheader("❌ Missing Skills")

        missing = jd_analysis.get("missing_skills", [])

        if missing:
            for skill in missing:
                st.error(skill)
        else:
            st.info("No missing skills found.")

        st.subheader("💪 Strengths")

        strengths = jd_analysis.get("strengths", [])

        if strengths:
            for strength in strengths:
                st.success(strength)
        else:
            st.info("No strengths found.")

        st.subheader("⚠ Weaknesses")

        weaknesses = jd_analysis.get("weaknesses", [])

        if weaknesses:
            for weakness in weaknesses:
                st.warning(weakness)
        else:
            st.info("No weaknesses found.")

        st.subheader("💡 Suggestions")

        suggestions = jd_analysis.get("suggestions", [])

        if suggestions:
            for suggestion in suggestions:
                st.markdown(f"✅ {suggestion}")
        else:
            st.info("No suggestions found.")

        st.subheader("📝 Resume Improvements")

        improvements = jd_analysis.get("resume_improvements", [])

        if improvements:
            for improvement in improvements:
                st.markdown(f"✔ {improvement}")
        else:
            st.info("No resume improvements found.")

st.markdown("---")

st.markdown(
    """
<div class="footer">

Built with ❤️ using

<b>Streamlit</b> •
<b>Groq</b> •
<b>LangChain</b> •
<b>FAISS</b> •
<b>HuggingFace</b>

<br><br>

© 2026 Chavadi Kiran Ganesh

</div>
""",
unsafe_allow_html=True
)