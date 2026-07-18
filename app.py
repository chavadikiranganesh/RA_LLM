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


# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="LLM-Powered Resume Analyzer using RAG",
    page_icon="🤖",
    layout="wide"
)


# ---------------- Custom CSS ---------------- #

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown(
    """
    <div class="title">
        🤖 LLM-Powered Resume Analyzer using RAG
    </div>

    <div class="subtitle">
        Analyze resumes using Large Language Models (LLMs),
        Retrieval-Augmented Generation (RAG),
        and AI-powered career insights.
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

    st.header("📂 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("📄 Processing Resume..."):
            st.session_state.vector_store = process_pdf(
                uploaded_file
            )

        st.session_state.messages = []
        st.session_state.chat_history = []

        st.success("✅ Resume uploaded successfully!")

    st.divider()

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    st.divider()

    st.subheader("💡 Example Questions")

    st.markdown("""
- 📄 Summarize my resume
- ⭐ ATS Score
- 💼 Which job suits me?
- 🎤 Generate interview questions
- 📝 Improve my resume
- 📚 Recommend certifications
- 📂 Explain my projects
- 💻 What are my technical skills?
- 📈 Do I qualify for a Data Engineer role?
""")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.chat_history = []

        st.rerun()


# ---------------- Welcome ---------------- #

if st.session_state.vector_store is None:

    st.info(
        "👈 Upload your resume from the sidebar to start chatting."
    )


# ---------------- Chat History ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])
# ---------------- Chat ---------------- #

question = st.chat_input("Ask anything about your resume...")

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
        with st.spinner("🤖 AI is analyzing your resume..."):

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

                st.subheader("📄 Resume Summary")
                st.write(assistant_reply)

            # ---------------- ATS ---------------- #

            elif intent == "ats":

                score = analysis.get("ats_score", 0)

                assistant_reply = f"ATS Score : {score}/100"

                st.metric(
                    "📊 ATS Score",
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


            elif intent == "skills":

                skills = analysis.get("skills", [])
                missing = analysis.get("missing_skills", [])

                assistant_reply = format_response(skills)

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("✅ Skills")

                    if isinstance(skills, list):
                        if skills:
                            for skill in skills:
                                st.success(skill)
                        else:
                            st.info("No skills found.")
                    else:
                        st.success(format_response(skills))

                with col2:

                    st.subheader("⚠ Missing Skills")

                    if isinstance(missing, list):
                        if missing:
                            for skill in missing:
                                st.warning(skill)
                        else:
                            st.info("No missing skills found.")
                    else:
                        st.warning(format_response(missing))


            elif intent == "interview":

                questions = analysis.get(
                    "interview_questions",
                    []
                )

                assistant_reply = format_response(questions)

                st.subheader("🎤 Interview Questions")

                if isinstance(questions, list):
                    if questions:
                        for q in questions:
                            st.info(q)
                    else:
                        st.info("No interview questions generated.")
                else:
                    st.info(format_response(questions))


            elif intent == "improve":

                improvements = analysis.get("resume_improvements", [])

                assistant_reply = format_response(improvements)

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


            elif intent == "certifications":

                certs = analysis.get(
                    "certifications",
                    []
                )

                assistant_reply = format_response(certs)

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

                st.subheader("📂 Projects")

                if isinstance(projects, list):

                    if projects:

                        for project in projects:

                            if isinstance(project, dict):

                                st.success(f"📂 {project.get('project_name', 'Project')}")

                                st.write(
                                    f"**Description:** {project.get('description', 'Not available')}"
                                )

                                st.caption(
                                    f"Technologies: {project.get('technologies', 'Not available')}"
                                )

                                st.divider()

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
                    "⬇ Download Report",
                    file,
                    "Resume_Report.pdf",
                    "application/pdf"
                )

            st.divider()

            with st.expander("📄 Retrieved Resume Chunks"):

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

if st.button("Compare Resume with JD"):

    if st.session_state.vector_store is None:

        st.warning("Please upload a resume.")

    elif job_description.strip() == "":

        st.warning("Please enter a Job Description.")

    else:

        with st.spinner(
            "Comparing Resume with Job Description..."
        ):

            jd_analysis = compare_resume(
                st.session_state.vector_store,
                job_description
            )

        st.success("Comparison Complete!")

        st.metric(
            "Match Score",
            f"{jd_analysis['match_score']}%"
        )

        st.progress(
            jd_analysis["match_score"] / 100
        )

        st.subheader("✅ Matching Skills")

        matching = jd_analysis.get("matching_skills", [])

        if matching:
            for skill in matching:
                st.success(skill)
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
                st.info(suggestion)
        else:
            st.info("No suggestions found.")

        st.subheader("📝 Resume Improvements")

        improvements = jd_analysis.get("resume_improvements", [])

        if improvements:
            for improvement in improvements:
                st.success(improvement)
        else:
            st.info("No resume improvements found.")