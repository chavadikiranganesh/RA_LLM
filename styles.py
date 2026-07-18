def load_css():
    return """
    <style>

    /* ---------------- Main App ---------------- */

    .stApp{
        background:#0f172a;
    }

    section.main > div{
        padding-top:1rem;
    }

    /* ---------------- Hero ---------------- */

    .hero{
    background:linear-gradient(135deg,#2563eb,#4f46e5);
    border-radius:24px;
    padding:40px;
    text-align:center;
    color:white;
}

    .title{
        font-size:46px;
        font-weight:800;
        color:white;
        margin-bottom:10px;
    }

    .subtitle{
        font-size:20px;
        color:#dbeafe;
        margin-bottom:15px;
    }

    .hero-text{
        font-size:18px;
        color:white;
        max-width:900px;
        margin:auto;
        line-height:1.8;
    }

    /* ---------------- Feature Cards ---------------- */

    .feature-grid{
        display:grid;
        grid-template-columns:repeat(4,1fr);
        gap:18px;
        margin-bottom:30px;
    }

    .feature-card{
        background:#1e293b;
        border-radius:20px;
        padding:25px;
        text-align:center;
        border:1px solid #334155;
        transition:.3s;
    }

    .feature-card:hover{
        transform:translateY(-8px);
        box-shadow:0 15px 30px rgba(0,0,0,.35);
    }

    .feature-icon{
        font-size:42px;
        margin-bottom:12px;
    }

    .feature-title{
        color:white;
        font-size:20px;
        font-weight:700;
    }

    .feature-text{
        color:#cbd5e1;
        margin-top:10px;
        font-size:14px;
    }

    /* ---------------- Chat ---------------- */

    .stChatMessage{
        border-radius:18px;
        padding:14px;
        margin-bottom:12px;
        border:1px solid #334155;
        background:#111827;
    }

    /* ---------------- Buttons ---------------- */

    .stButton>button{
        width:100%;
        border-radius:12px;
        height:48px;
        font-weight:700;
        background:#2563eb;
        color:white;
        border:none;
        transition:.3s;
    }

    .stButton>button:hover{
        background:#1d4ed8;
        transform:translateY(-2px);
    }

    /* ---------------- Download Button ---------------- */

    .stDownloadButton>button{
        width:100%;
        border-radius:12px;
        background:#10b981;
        color:white;
        border:none;
        font-weight:700;
        height:45px;
    }

    .stDownloadButton>button:hover{
        background:#059669;
    }

    /* ---------------- Sidebar ---------------- */

    section[data-testid="stSidebar"]{
        background:#1e293b;
        border-right:1px solid #334155;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3{
        color:white;
    }

    /* ---------------- File Upload ---------------- */

    .stFileUploader{
        border:2px dashed #3b82f6;
        border-radius:15px;
        padding:10px;
    }

    /* ---------------- Skill Chips ---------------- */

    .skill-chip{
        display:inline-block;
        background:#2563eb;
        color:white;
        padding:8px 16px;
        margin:5px;
        border-radius:25px;
        font-size:14px;
        font-weight:600;
        transition:.2s;
    }

    .skill-chip:hover{
        background:#1d4ed8;
    }

    /* ---------------- Project Cards ---------------- */

    .project-card{
        background:#1e293b;
        border-radius:20px;
        padding:22px;
        margin-bottom:18px;
        border-left:5px solid #3b82f6;
        border:1px solid #334155;
        transition:.3s;
    }

    .project-card:hover{
        transform:translateY(-5px);
        box-shadow:0 10px 25px rgba(0,0,0,.25);
    }

    .project-title{
        font-size:22px;
        font-weight:700;
        color:white;
        margin-bottom:12px;
    }

    .project-desc{
        color:#cbd5e1;
        line-height:1.7;
        margin-bottom:15px;
    }

    .tech-chip{
        display:inline-block;
        background:#2563eb;
        color:white;
        padding:6px 12px;
        border-radius:20px;
        margin:4px;
        font-size:13px;
        font-weight:600;
    }

    /* ---------------- Metrics ---------------- */

    div[data-testid="stMetric"]{
        background:#1e293b;
        padding:18px;
        border-radius:18px;
        border:1px solid #334155;
    }

    /* ---------------- Expanders ---------------- */

    .streamlit-expanderHeader{
        font-weight:700;
    }

    /* ---------------- Footer ---------------- */

    .footer{
        margin-top:40px;
        text-align:center;
        color:#94a3b8;
        font-size:14px;
        padding:20px;
    }

    hr{
        border:none;
        height:1px;
        background:#334155;
    }

    </style>
    """