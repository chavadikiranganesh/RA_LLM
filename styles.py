def load_css():
    return """
    <style>

    /* ==========================================================
       Main App
    ========================================================== */

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    /* ==========================================================
       Cards
    ========================================================== */

    div[data-testid="stMetric"],
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMetric"]){

        border-radius:15px;
        border:1px solid rgba(128,128,128,0.25);
        padding:15px;
    }

    /* ==========================================================
       Sidebar
    ========================================================== */

    section[data-testid="stSidebar"]{
        border-right:1px solid rgba(128,128,128,0.2);
    }

    /* ==========================================================
       Buttons
    ========================================================== */

    .stButton>button{

        width:100%;
        height:48px;
        border-radius:12px;
        border:none;
        background:#2563EB;
        color:white;
        font-weight:600;
        transition:0.3s;
    }

    .stButton>button:hover{

        background:#1D4ED8;
        transform:translateY(-2px);
    }

    /* ==========================================================
       Download Button
    ========================================================== */

    .stDownloadButton>button{

        width:100%;
        height:48px;
        border-radius:12px;
        border:none;
        background:#10B981;
        color:white;
        font-weight:600;
        transition:0.3s;
    }

    .stDownloadButton>button:hover{

        background:#059669;
        transform:translateY(-2px);
    }

    /* ==========================================================
       Chat
    ========================================================== */

    div[data-testid="stChatMessage"]{

        border-radius:15px;
        border:1px solid rgba(128,128,128,0.25);
        padding:12px;
        margin-bottom:10px;
    }

    /* ==========================================================
       File Uploader
    ========================================================== */

    .stFileUploader{

        border:2px dashed #3B82F6;
        border-radius:15px;
        padding:12px;
    }

    /* ==========================================================
       Expander
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
        background:rgba(128,128,128,0.3);
    }

    </style>
    """