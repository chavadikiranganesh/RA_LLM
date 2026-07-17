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

    story.append(Paragraph("<b>AI Resume Analysis Report</b>", styles["Title"]))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {analysis['ats_score']}/100",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Resume Summary</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            analysis["summary"],
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Strengths</b>",
            styles["Heading2"]
        )
    )

    for s in analysis["strengths"]:
        story.append(
            Paragraph("• " + s, styles["BodyText"])
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Weaknesses</b>",
            styles["Heading2"]
        )
    )

    for s in analysis["weaknesses"]:
        story.append(
            Paragraph("• " + s, styles["BodyText"])
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Recommended Roles</b>",
            styles["Heading2"]
        )
    )

    for s in analysis["recommended_roles"]:
        story.append(
            Paragraph("• " + s, styles["BodyText"])
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    for s in analysis["missing_skills"]:
        story.append(
            Paragraph("• " + s, styles["BodyText"])
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Interview Questions</b>",
            styles["Heading2"]
        )
    )

    for s in analysis["interview_questions"]:
        story.append(
            Paragraph("• " + s, styles["BodyText"])
        )

    doc.build(story)

    return filename