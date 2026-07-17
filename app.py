from report_generator import create_pdf
from styles import load_css

import streamlit as st

from utils import process_pdf
from chatbot import ask_resume, compare_resume
from intent import detect_intent


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

        if st.session_state.vector_store is None:

            with st.spinner("📄 Processing Resume..."):

                st.session_state.vector_store = process_pdf(
                    uploaded_file
                )

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

                roles = analysis.get(
                    "recommended_roles",
                    []
                )

                assistant_reply = "\n".join(roles)

                st.subheader("💼 Recommended Roles")

                for role in roles:
                    st.success(role)

            # ---------------- SKILLS ---------------- #

            elif intent == "skills":

                skills = analysis.get("skills", [])
                missing = analysis.get("missing_skills", [])

                assistant_reply = "\n".join(skills)

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader("✅ Skills")

                    for skill in skills:
                        st.success(skill)

                with col2:

                    st.subheader("⚠ Missing Skills")

                    for skill in missing:
                        st.warning(skill)

            # ---------------- INTERVIEW ---------------- #

            elif intent == "interview":

                questions = analysis.get(
                    "interview_questions",
                    []
                )

                assistant_reply = "\n".join(questions)

                st.subheader("🎤 Interview Questions")

                for q in questions:
                    st.info(q)

            # ---------------- IMPROVEMENTS ---------------- #

            elif intent == "improve":

                improvements = analysis.get(
                    "resume_improvements",
                    []
                )

                assistant_reply = "\n".join(improvements)

                st.subheader("📝 Resume Improvements")

                for tip in improvements:
                    st.success(tip)

            # ---------------- CERTIFICATIONS ---------------- #

            elif intent == "certifications":

                certs = analysis.get(
                    "certifications",
                    []
                )

                assistant_reply = "\n".join(certs)

                st.subheader("📚 Recommended Certifications")

                for cert in certs:
                    st.info(cert)

            # ---------------- PROJECTS ---------------- #

            elif intent == "projects":

                projects = analysis.get(
                    "projects",
                    []
                )

                assistant_reply = "\n".join(projects)

                st.subheader("📂 Projects")

                for project in projects:
                    st.success(project)

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

        for skill in jd_analysis.get(
            "matching_skills",
            []
        ):
            st.success(skill)

        st.subheader("❌ Missing Skills")

        for skill in jd_analysis.get(
            "missing_skills",
            []
        ):
            st.error(skill)

        st.subheader("💪 Strengths")

        for strength in jd_analysis.get(
            "strengths",
            []
        ):
            st.success(strength)

        st.subheader("⚠ Weaknesses")

        for weakness in jd_analysis.get(
            "weaknesses",
            []
        ):
            st.warning(weakness)

        st.subheader("💡 Suggestions")

        for suggestion in jd_analysis.get(
            "suggestions",
            []
        ):
            st.info(suggestion)

        st.subheader("📝 Resume Improvements")

        for improvement in jd_analysis.get(
            "resume_improvements",
            []
        ):
            st.success(improvement)