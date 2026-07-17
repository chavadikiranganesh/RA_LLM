from report_generator import create_pdf
from styles import load_css

import streamlit as st

from utils import process_pdf
from chatbot import ask_resume, compare_resume


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
    <div class="title">🤖 LLM-Powered Resume Analyzer using RAG</div>
    <div class="subtitle">
        Analyze resumes using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI-powered career insights.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.header("📂 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("📄 Reading Resume..."):
            st.session_state.vector_store = process_pdf(uploaded_file)

        st.success("✅ Resume uploaded successfully!")

    st.divider()

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    st.divider()

    st.subheader("💡 Try Asking")

    st.markdown("""
- 📄 Summarize my resume
- ⭐ Rate my skills
- 🎯 ATS Score
- 💼 Which job roles suit me?
- ❌ What skills are missing?
- 📚 Recommend certifications
- 🎤 Generate interview questions
- 📝 Improve my resume
""")

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- Welcome ---------------- #

if st.session_state.vector_store is None:
    st.info("👈 Upload your resume from the sidebar.")

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

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("🤖 AI is analyzing your resume..."):

            analysis, docs = ask_resume(
                question,
                st.session_state.vector_store
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": analysis["summary"]
            }
        )

        with st.chat_message("assistant"):

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "📊 ATS Score",
                    f"{analysis['ats_score']}/100"
                )
                st.progress(analysis["ats_score"] / 100)

            with col2:
                st.metric(
                    "💼 Best Role",
                    analysis["recommended_roles"][0]
                    if analysis["recommended_roles"]
                    else "-"
                )

            st.divider()

            st.subheader("📄 Resume Summary")
            st.write(analysis["summary"])

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Strengths")
                for item in analysis["strengths"]:
                    st.success(item)

            with col2:
                st.subheader("⚠ Weaknesses")
                for item in analysis["weaknesses"]:
                    st.error(item)

            st.divider()

            st.subheader("💼 Recommended Roles")

            for role in analysis["recommended_roles"]:
                st.success(role)

            st.divider()

            st.subheader("📚 Missing Skills")

            for skill in analysis["missing_skills"]:
                st.warning(skill)

            st.divider()

            st.subheader("🎤 Interview Questions")

            for q in analysis["interview_questions"]:
                st.info(q)

            st.divider()

            pdf_file = create_pdf(analysis)

            with open(pdf_file, "rb") as file:

                st.download_button(
                    "⬇ Download Resume Report",
                    file,
                    "Resume_Report.pdf",
                    "application/pdf"
                )

            st.divider()

            with st.expander("📄 Retrieved Resume Sections"):

                for i, doc in enumerate(docs, start=1):
                    st.markdown(f"### Chunk {i}")
                    st.write(doc.page_content)
                    st.divider()

# ======================================================
# Resume vs Job Description Matching
# ======================================================

st.divider()

st.header("🎯 Resume vs Job Description Match")

if st.button("Compare Resume with JD"):

    if st.session_state.vector_store is None:

        st.warning("Please upload a resume.")

    elif job_description.strip() == "":

        st.warning("Please paste a Job Description.")

    else:

        with st.spinner("Comparing Resume with Job Description..."):

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

        for skill in jd_analysis["matching_skills"]:
            st.success(skill)

        st.subheader("❌ Missing Skills")

        for skill in jd_analysis["missing_skills"]:
            st.error(skill)

        st.subheader("💪 Strengths")

        for s in jd_analysis["strengths"]:
            st.success(s)

        st.subheader("⚠ Weaknesses")

        for w in jd_analysis["weaknesses"]:
            st.warning(w)

        st.subheader("💡 Suggestions")

        for tip in jd_analysis["suggestions"]:
            st.info(tip)

        st.divider()

        # ---------------- Resume Improvements ---------------- #

        st.subheader("📝 Resume Improvements")

        for improvement in jd_analysis.get("resume_improvements", []):
            st.success(improvement)