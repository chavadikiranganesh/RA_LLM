# ==========================================================
# Imports
# ==========================================================

import streamlit as st

from report_generator import create_pdf
from styles import load_css
from utils import process_pdf
from chatbot import ask_resume, compare_resume
from intent import detect_intent


# ==========================================================
# Helper Functions
# ==========================================================

def format_response(value):
    """
    Convert any response into a readable string.
    """

    if value is None:
        return ""

    if isinstance(value, list):
        return "\n".join(str(item) for item in value)

    if isinstance(value, dict):
        return "\n".join(
            f"{key}: {val}"
            for key, val in value.items()
        )

    return str(value)


# ==========================================================
# Display Skill Chips
# ==========================================================

def display_chips(items, chip_type="success"):
    """
    Display a list of items as colored badges.
    """

    if not items:

        st.info("No items found.")
        return

    if isinstance(items, str):
        items = [items]

    columns = st.columns(
        min(4, max(1, len(items)))
    )

    for index, item in enumerate(items):

        with columns[index % len(columns)]:

            if chip_type == "success":
                st.success(item)

            elif chip_type == "warning":
                st.warning(item)

            elif chip_type == "error":
                st.error(item)

            else:
                st.info(item)


# ==========================================================
# Display Project Card
# ==========================================================

def display_project(project):
    """
    Display a project beautifully regardless of
    the LLM output format.
    """

    if not isinstance(project, dict):

        st.info(str(project))
        return

    project_name = (
        project.get("project_name")
        or project.get("Project Name")
        or project.get("project")
        or "Project"
    )

    description = (
        project.get("description")
        or project.get("Description")
        or project.get("One-line description")
        or "No description available."
    )

    technologies = (
        project.get("technologies")
        or project.get("Technologies used")
        or project.get("tech_stack")
        or []
    )

    if isinstance(technologies, str):

        technologies = (
            technologies
            .replace("|", ",")
            .replace("•", ",")
        )

        technologies = [
            tech.strip()
            for tech in technologies.split(",")
            if tech.strip()
        ]

    with st.container(border=True):

        st.subheader(f"📂 {project_name}")

        st.write(description)

        if technologies:

            st.markdown("#### 🛠 Technologies")

            tech_columns = st.columns(
                min(4, len(technologies))
            )

            for index, tech in enumerate(technologies):

                with tech_columns[index % len(tech_columns)]:
                    st.info(tech)


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(

    page_title="AI Resume Analyzer",

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"
)


# ==========================================================
# Load Custom CSS
# ==========================================================

st.markdown(
    load_css(),
    unsafe_allow_html=True
)


# ==========================================================
# Session State
# ==========================================================

defaults = {

    "vector_store": None,

    "messages": [],

    "chat_history": [],

    "analysis": None,

    "uploaded_resume": False,

    "uploaded_filename": None

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# Header
# ==========================================================

st.title("🤖 AI Resume Analyzer")

st.caption(
    "Powered by Llama 3.3 • Groq • LangChain • HuggingFace • FAISS"
)

st.markdown("""
<div style="text-align:center">

# 🚀 Your AI Career Assistant

Analyze your resume using AI.

📄 Resume Summary • 💻 Skills • 🎯 JD Match

---

⬅️ Upload your PDF Resume from the left sidebar to get started.

</div>
""", unsafe_allow_html=True)

st.divider()


# ==========================================================
# AI Feature Dashboard
# ==========================================================

st.subheader("✨ Core Features")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("## 📄")
        st.markdown("### Resume Summary")
        st.caption("AI-generated summary")

    with st.container(border=True):
        st.markdown("## 💻")
        st.markdown("### Skills Analysis")
        st.caption("Skills & Missing Skills")

with col2:
    with st.container(border=True):
        st.markdown("## 🎯")
        st.markdown("### ATS Analysis")
        st.caption("ATS Score & Keywords")

    with st.container(border=True):
        st.markdown("## 💼")
        st.markdown("### Job Roles")
        st.caption("AI Career Suggestions")

with col3:
    with st.container(border=True):
        st.markdown("## 🤖")
        st.markdown("### Resume Chat")
        st.caption("Chat with your Resume")

    with st.container(border=True):
        st.markdown("## 🎯")
        st.markdown("### JD Matching")
        st.caption("Compare with Job Description")

st.divider()


# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:

    st.header("Upload Resume")

    st.caption("Upload your PDF resume to start the AI analysis.")

    uploaded_file = st.file_uploader(

        "Choose Resume",

        type=["pdf"]

    )

    if uploaded_file is not None:

        current_file = (
            uploaded_file.name,
            uploaded_file.size
        )

        previous_file = st.session_state.get(
            "uploaded_filename"
        )

        if current_file != previous_file:

            with st.spinner(
                "Processing resume..."
            ):

                st.session_state.vector_store = process_pdf(
                    uploaded_file
                )

            st.session_state.uploaded_filename = current_file

            st.session_state.uploaded_resume = True

            st.session_state.messages = []

            st.session_state.chat_history = []

            st.session_state.analysis = None

            st.success(
                "Resume uploaded successfully!"
            )

    st.divider()

    # ------------------------------------------------------

    st.header("Job Description")

    job_description = st.text_area(

        "Paste Job Description",

        height=220,

        placeholder="Paste the complete Job Description here..."

    )

    st.divider()

    # ------------------------------------------------------

    st.header("Quick Questions")

    quick_questions = [

        "Summarize my resume",

        "Give my ATS score",

        "Show my technical skills",

        "Recommend suitable roles",

        "Explain my projects",

        "Generate interview questions",

        "Suggest certifications",

        "Improve my resume"

    ]

    for item in quick_questions:

        st.info(item)

    st.divider()

    # ------------------------------------------------------

    st.header("Tech Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.success("Groq")
        st.success("LangChain")
        st.success("FAISS")

    with col2:
        st.success("Llama 3.3")
        st.success("Hugging Face")
        st.success("Streamlit")

    st.divider()

    if st.button(

        "Clear Chat",

        use_container_width=True

    ):

        st.session_state.messages = []

        st.session_state.chat_history = []

        st.session_state.analysis = None

        st.rerun()
        # ==========================================================
# Welcome Screen
# ==========================================================

if st.session_state.vector_store is None:

    with st.container(border=True):

                st.markdown("# 👋 Welcome")

                st.write(
                    "Upload your resume and unlock AI-powered career insights "
                    "using Llama 3.3, Groq, LangChain and RAG."
                )

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.success("📄 Resume Summary")
                    st.success("🎯 ATS Score")
                    st.success("💻 Skills Analysis")
                    st.success("💼 Job Role Recommendation")
                    st.success("📂 Project Analysis")

                with col2:
                    st.success("🎤 Interview Questions")
                    st.success("📚 Certification Suggestions")
                    st.success("📝 Resume Improvements")
                    st.success("🤖 Resume Chatbot")
                    st.success("🎯 Resume vs JD Matching")

                st.divider()

                st.info("⬅️ Upload your PDF resume from the sidebar to begin.")


# ==========================================================
# Chat History
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================================
# Example Prompts
# ==========================================================

if st.session_state.vector_store:

    st.markdown("### Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("Summarize my resume")
        st.info("Show my technical skills")
        st.info("Recommend suitable roles")

    with col2:
        st.info("Explain my projects")
        st.info("Generate interview questions")
        st.info("Suggest certifications")

    with col3:
        st.info("Improve my resume")
        st.info("Compare with a Job Description")
        st.info("What is my strongest skill?")


# ==========================================================
# Chat Input
# ==========================================================

question = st.chat_input(
    "💬 Ask anything about your resume..."
)


# ==========================================================
# AI Resume Processing
# ==========================================================

if question:

    if st.session_state.vector_store is None:

        st.warning("⚠️ Please upload your resume first.")

    else:

        intent = detect_intent(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.spinner(
            "🤖 Reading Resume • Searching Knowledge Base • Generating Response..."
        ):

            analysis, docs = ask_resume(
                question,
                st.session_state.vector_store,
                intent,
                st.session_state.chat_history
            )

            st.session_state.analysis = analysis

        with st.chat_message("assistant"):

            # ======================================================
            # Resume Summary
            # ======================================================

            if intent == "summary":
                assistant_reply = analysis.get(
                    "summary",
                    "No summary generated."
                )
                with st.container(border=True):
                    st.subheader("📄 Resume Summary")
                    st.write(assistant_reply)

            # ======================================================
            # ATS Score
            # ======================================================

            elif intent == "ats":
                score = max(
                    0,
                    min(
                        100,
                        analysis.get("ats_score", 0)
                    )
                )
                assistant_reply = f"ATS Score: {score}/100"
                with st.container(border=True):
                    st.subheader("🎯 ATS Analysis")
                    st.metric(
                        "Overall ATS Score",
                        f"{score}/100"
                    )
                    st.progress(score / 100)
                    st.info(
                        analysis.get(
                            "reason",
                            "No explanation available."
                        )
                    )

            # ======================================================
            # Skills Analysis
            # ======================================================

            elif intent == "skills":
                skills = analysis.get(
                    "skills",
                    []
                )
                missing = analysis.get(
                    "missing_skills",
                    []
                )
                assistant_reply = format_response(skills)
                with st.container(border=True):
                    st.subheader("💻 Skills Analysis")
                    left, right = st.columns(2)
                    with left:
                        st.markdown("### ✅ Existing Skills")
                        if isinstance(skills, list):
                            display_chips(
                                skills,
                                "success"
                            )
                        else:
                            st.write(
                                format_response(skills)
                            )
                    with right:
                        st.markdown("### ⚠️ Missing Skills")
                        if isinstance(missing, list):
                            display_chips(
                                missing,
                                "warning"
                            )
                        else:
                            st.write(
                                format_response(missing)
                            )

            # ======================================================
            # Recommended Roles
            # ======================================================

            elif intent == "roles":
                roles = analysis.get(
                    "recommended_roles",
                    []
                )
                assistant_reply = format_response(roles)
                with st.container(border=True):
                    st.subheader("💼 Recommended Roles")
                    if isinstance(roles, list):
                        if roles:
                            for role in roles:
                                st.success(role)
                        else:
                            st.info(
                                "No recommended roles found."
                            )
                    else:
                        st.write(
                            format_response(roles)
                        )

            # ======================================================
            # Experience
            # ======================================================

            elif intent == "experience":
                assistant_reply = analysis.get(
                    "experience",
                    "No experience information found."
                )
                with st.container(border=True):
                    st.subheader("💼 Experience")
                    st.write(assistant_reply)

            # ======================================================
            # Projects
            # ======================================================

            elif intent == "projects":
                projects = analysis.get(
                    "projects",
                    []
                )
                assistant_reply = format_response(projects)
                with st.container(border=True):
                    st.subheader("📂 Projects")
                    if isinstance(projects, list):
                        if projects:
                            for project in projects:
                                display_project(project)
                        else:
                            st.info(
                                "No projects found."
                            )
                    elif isinstance(projects, dict):
                        display_project(projects)
                    else:
                        st.write(
                            format_response(projects)
                        )

            # ======================================================
            # Interview Questions
            # ======================================================

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
                            for index, question_item in enumerate(
                                questions,
                                start=1
                            ):
                                st.info(
                                    f"**Q{index}.** {question_item}"
                                )
                        else:
                            st.info(
                                "No interview questions generated."
                            )
                    else:
                        st.write(
                            format_response(questions)
                        )

            # ======================================================
            # Resume Improvements
            # ======================================================

            elif intent == "improve":
                improvements = analysis.get(
                    "resume_improvements",
                    []
                )
                assistant_reply = format_response(improvements)
                with st.container(border=True):
                    st.subheader("📝 Resume Improvements")
                    if isinstance(improvements, list):
                        if improvements:
                            for item in improvements:
                                st.success(item)
                        else:
                            st.info(
                                "No improvement suggestions available."
                            )
                    else:
                        st.write(
                            format_response(improvements)
                        )

            # ======================================================
            # Certifications
            # ======================================================

            elif intent == "certifications":
                certifications = analysis.get(
                    "certifications",
                    []
                )
                assistant_reply = format_response(certifications)
                with st.container(border=True):
                    st.subheader(
                        "📚 Recommended Certifications"
                    )
                    if isinstance(certifications, list):
                        if certifications:
                            for cert in certifications:
                                st.info(cert)
                        else:
                            st.info(
                                "No certifications suggested."
                            )
                    else:
                        st.write(
                            format_response(certifications)
                        )

            # ======================================================
            # General Chat
            # ======================================================

            else:
                assistant_reply = analysis.get(
                    "answer",
                    "No response generated."
                )

                with st.container(border=True):
                    st.subheader("🤖 AI Response")
                    st.write(assistant_reply)

            # ======================================================
            # Download PDF Report
            # ======================================================

            st.divider()

            try:
                pdf_file = create_pdf(analysis)

                with open(pdf_file, "rb") as pdf:
                    st.download_button(
                        label="📥 Download Resume Report",
                        data=pdf,
                        file_name="Resume_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

            except Exception as error:
                st.warning(f"Unable to generate report: {error}")

            # ======================================================
            # Retrieved Resume Context (RAG)
            # ======================================================

            if docs:
                with st.expander(
                    "🔍 Retrieved Resume Context (RAG)",
                    expanded=False
                ):
                    for index, doc in enumerate(docs, start=1):
                        st.markdown(f"### Chunk {index}")
                        st.write(doc.page_content)
                        st.divider()

            # ======================================================
            # Save Conversation
            # ======================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )

            st.session_state.chat_history.append(
                ("Human", question)
            )

            st.session_state.chat_history.append(
                ("AI", assistant_reply)
            )


# ==========================================================
# Resume vs Job Description Matching
# ==========================================================

st.divider()
st.header("🎯 Resume vs Job Description Matching")
st.caption("Compare your resume with a Job Description using AI.")

if st.button("🚀 Compare Resume with Job Description", use_container_width=True):

    if st.session_state.vector_store is None:
        st.warning("⚠️ Please upload your resume first.")

    elif not job_description.strip():
        st.warning("⚠️ Please paste a Job Description.")

    else:
        with st.spinner("🔍 Comparing Resume with Job Description..."):
            jd_analysis = compare_resume(
                st.session_state.vector_store,
                job_description
            )

        st.success("✅ Comparison Completed!")

        # ==================================================
        # Match Score
        # ==================================================

        score = max(
            0,
            min(100, jd_analysis.get("match_score", 0))
        )

        with st.container(border=True):
            st.subheader("🎯 Match Score")
            st.metric("Resume Match", f"{score}%")
            st.progress(score / 100)

        # ==================================================
        # Skills Comparison
        # ==================================================

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("✅ Matching Skills")
                matching = jd_analysis.get("matching_skills", [])
                display_chips(matching, "success")

        with col2:
            with st.container(border=True):
                st.subheader("❌ Missing Skills")
                missing = jd_analysis.get("missing_skills", [])
                display_chips(missing, "error")

        col3, col4 = st.columns(2)

        with col3:
            with st.container(border=True):
                st.subheader("💪 Strengths")
                strengths = jd_analysis.get("strengths", [])

                if strengths:
                    for strength in strengths:
                        st.success(strength)
                else:
                    st.info("No strengths found.")

        with col4:
            with st.container(border=True):
                st.subheader("⚠️ Weaknesses")
                weaknesses = jd_analysis.get("weaknesses", [])

                if weaknesses:
                    for weakness in weaknesses:
                        st.warning(weakness)
                else:
                    st.info("No weaknesses found.")

        # ==================================================
        # Suggestions
        # ==================================================

        with st.container(border=True):
            st.subheader("💡 Suggestions")

            suggestions = jd_analysis.get("suggestions", [])

            if suggestions:
                for suggestion in suggestions:
                    st.success(suggestion)
            else:
                st.info("No suggestions available.")

        # ==================================================
        # Resume Improvements
        # ==================================================

        with st.container(border=True):
            st.subheader("📝 Resume Improvements")

            improvements = jd_analysis.get("resume_improvements", [])

            if improvements:
                for improvement in improvements:
                    st.success(improvement)
            else:
                st.info("No improvements suggested.")

        # ==================================================
        # ATS Keyword Coverage
        # ==================================================

        with st.container(border=True):
            st.subheader("📌 ATS Keyword Coverage")

            ats_keywords = jd_analysis.get("ats_keywords", [])

            if ats_keywords:
                for item in ats_keywords:
                    keyword = item.get("keyword", "")
                    status = item.get("status", "")
                    importance = item.get("importance", "")

                    text = f"{keyword} ({importance})"

                    if status == "Matched":
                        st.success(f"✅ {text}")
                    else:
                        st.error(f"❌ {text}")
            else:
                st.info("No ATS keyword analysis available.")


# ==================================================
# Footer
# ==================================================

st.markdown(
    """
    <div style="text-align:center;">

    <h3>🤖 AI Resume Analyzer</h3>

    <p>
        Powered by
        <strong>Groq</strong> •
        <strong>LangChain</strong> •
        <strong>HuggingFace</strong> •
        <strong>FAISS</strong>
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)
