from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(analysis):

    filename = "Resume_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # ---------- ATS ----------

    if analysis.get("ats_score") is not None:

        story.append(
            Paragraph(
                f"<b>ATS Score:</b> {analysis.get('ats_score')}/100",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 12))

    # ---------- Summary ----------

    if analysis.get("summary"):

        story.append(
            Paragraph(
                "<b>Resume Summary</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                analysis.get("summary"),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 12))

    # ---------- Answer ----------

    if analysis.get("answer"):

        story.append(
            Paragraph(
                "<b>Answer</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                analysis.get("answer"),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 12))

    # ---------- Helper ----------

    def add_list(title, items):

        if items:

            story.append(
                Paragraph(
                    f"<b>{title}</b>",
                    styles["Heading2"]
                )
            )

            for item in items:

                story.append(
                    Paragraph(
                        "• " + str(item),
                        styles["BodyText"]
                    )
                )

            story.append(Spacer(1, 12))

    # ---------- Lists ----------

    add_list("Skills", analysis.get("skills", []))
    add_list("Missing Skills", analysis.get("missing_skills", []))
    add_list("Strengths", analysis.get("strengths", []))
    add_list("Weaknesses", analysis.get("weaknesses", []))
    add_list("Recommended Roles", analysis.get("recommended_roles", []))
    add_list("Interview Questions", analysis.get("interview_questions", []))
    add_list("Resume Improvements", analysis.get("resume_improvements", []))
    add_list("Certifications", analysis.get("certifications", []))
    add_list("Projects", analysis.get("projects", []))
    add_list("Suggestions", analysis.get("suggestions", []))
    add_list("Matching Skills", analysis.get("matching_skills", []))

    # ---------- Experience ----------

    if analysis.get("experience"):

        story.append(
            Paragraph(
                "<b>Experience</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                analysis.get("experience"),
                styles["BodyText"]
            )
        )

    doc.build(story)

    return filename