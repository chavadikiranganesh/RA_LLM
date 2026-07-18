def load_css():
    return """
    <style>

    .main {
        padding-top: 1rem;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }

    .stButton>button {
        width:100%;
        border-radius:10px;
        height:45px;
        font-weight:bold;
    }

    .stFileUploader {
        border:2px dashed #4CAF50;
        border-radius:10px;
        padding:10px;
    }

    .title {
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:#4CAF50;
    }

    .subtitle {
        text-align:center;
        color:gray;
        font-size:18px;
        margin-bottom:25px;
    }

    /* ---------- Skill Chips ---------- */

    .skill-chip {
        display: inline-block;
        background: #2563eb;
        color: white;
        padding: 8px 14px;
        margin: 6px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 3px 8px rgba(37, 99, 235, .25);
    }

    /* ---------- Project Cards ---------- */

    .project-card {
        background: white;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 8px 20px rgba(0, 0, 0, .08);
    }

    .project-title {
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 12px;
    }

    .project-desc {
        color: #4b5563;
        line-height: 1.7;
        margin-bottom: 12px;
    }

    .tech-chip {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 6px 12px;
        border-radius: 18px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
    }

    </style>
    """