def load_css():
    return """
    <style>

    /* ==========================================================
       Main App
    ========================================================== */

    .stApp{
        background-color:#0F172A;
    }

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    /* ==========================================================
       Sidebar
    ========================================================== */

    section[data-testid="stSidebar"]{
        background:#1E293B;
        border-right:1px solid #334155;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4{
        color:white;
    }

    /* ==========================================================
       Buttons
    ========================================================== */

    .stButton>button{

        width:100%;
        border-radius:12px;
        height:48px;
        font-weight:600;
        background:#2563EB;
        color:white;
        border:none;
    }

    .stButton>button:hover{

        background:#1D4ED8;
    }

    /* ==========================================================
       Download Button
    ========================================================== */

    .stDownloadButton>button{

        width:100%;
        border-radius:12px;
        height:48px;
        background:#10B981;
        color:white;
        border:none;
        font-weight:600;
    }

    .stDownloadButton>button:hover{

        background:#059669;
    }

    /* ==========================================================
       Chat
    ========================================================== */

    div[data-testid="stChatMessage"]{

        border-radius:15px;
        border:1px solid #334155;
        padding:10px;
        margin-bottom:10px;
    }

    /* ==========================================================
       Metric Cards
    ========================================================== */

    div[data-testid="stMetric"]{

        background:#1E293B;
        border:1px solid #334155;
        border-radius:15px;
        padding:18px;
    }

    /* ==========================================================
       File Uploader
    ========================================================== */

    .stFileUploader{

        border:2px dashed #3B82F6;
        border-radius:15px;
        padding:10px;
    }

    /* ==========================================================
       Progress Bar
    ========================================================== */

    div[data-testid="stProgress"]{

        margin-top:10px;
        margin-bottom:10px;
    }

    /* ==========================================================
       Expanders
    ========================================================== */

    details{

        border-radius:12px;
    }

    /* ==========================================================
       Divider
    ========================================================== */

    hr{

        border:none;
        height:1px;
        background:#334155;
    }

    </style>
    """