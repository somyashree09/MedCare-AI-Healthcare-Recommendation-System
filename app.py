import streamlit as st

st.set_page_config(
    page_title="MedCare AI – Healthcare Recommendation System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
            

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B7285 0%, #0a5f6e 100%) !important;
    border-right: none;
    min-width: 280px !important;
    width: 280px !important;
}

[data-testid="stSidebarCollapsedControl"] {
    position: fixed !important;
    top: 70px !important;      /* adjust vertically */
    left: 0px !important;      /* stick to extreme left */
    z-index: 9999 !important;

    background: #0B7285 !important;
    border-radius: 0 8px 8px 0 !important;
    padding: 6px !important;
}

[data-testid="stSidebarCollapsedControl"] svg {
    color: white !important;
    fill: white !important;
}
[data-testid="stSidebarCollapsedControl"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
}

div[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: rgba(255,255,255,0.85) !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 8px 12px !important;
    border-radius: 6px !important;
    width: 100% !important;
    box-shadow: none !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
}
.main .stButton > button {
    background: #0B7285 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
.main .stButton > button:hover {
    background: #095f6e !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

# ── SIDEBAR (always rendered on every page) ──────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;padding:4px 0 16px;'
        'border-bottom:1px solid rgba(255,255,255,0.15);margin-bottom:12px;">'
        '<div style="width:32px;height:32px;background:rgba(255,255,255,0.15);border-radius:8px;'
        'display:flex;align-items:center;justify-content:center;">'
        '<span style="color:white;font-size:16px;">🩺</span></div>'
        '<div><div style="font-size:14px;font-weight:600;color:#ffffff;line-height:1.2;">MedCare AI</div>'
        '<div style="font-size:10px;color:rgba(255,255,255,0.6);">Healthcare System</div></div></div>'
        '<div style="font-size:10px;color:rgba(255,255,255,0.5);text-transform:uppercase;'
        'letter-spacing:1px;margin-bottom:6px;padding-left:4px;">Navigation</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.logged_in:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.12);border-radius:8px;padding:8px 12px;'
            f'margin-bottom:10px;display:flex;align-items:center;gap:8px;">'
            f'<div style="width:26px;height:26px;background:rgba(255,255,255,0.25);border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center;font-size:12px;color:white;font-weight:700;">'
            f'{st.session_state.current_user[0].upper()}</div>'
            f'<div><div style="font-size:11px;font-weight:600;color:#ffffff;">{st.session_state.current_user}</div>'
            f'<div style="font-size:9px;color:rgba(255,255,255,0.6);">Logged in</div></div></div>',
            unsafe_allow_html=True,
        )

    nav_items = [
        ("🏠  Home",                    "home"),
        ("🔐  Login",                   "login"),
        ("📝  Signup",                  "signup"),
        ("🩺  Disease Prediction",      "disease"),
        ("💊  Medicine Recommendation", "medicine"),
        ("🥗  Diet Recommendation",     "diet"),
        ("📊  Dashboard",               "dashboard"),
        ("🕑  History",                 "history"),
        ("📥  Download Report",         "report"),
    ]

    for label, key in nav_items:
        if st.session_state.page == key:
            st.markdown(
                f'<div style="background:rgba(255,255,255,0.18);border-radius:6px;'
                f'border-right:3px solid #ffffff;margin-bottom:2px;">'
                f'<span style="font-size:13px;color:#ffffff;font-weight:600;'
                f'padding:8px 12px;display:block;">{label}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(label, key=f"sidebar_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    if st.session_state.logged_in:
        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = "login"
            st.rerun()

# ── PAGE ROUTING ──────────────────────────────────────────────────────────────
from pages_ import home, login, signup, disease, medicine, diet, dashboard, history, report

if st.session_state.page == "home":
    home.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "signup":
    signup.show()
elif st.session_state.page == "disease":
    disease.show()
elif st.session_state.page == "medicine":
    medicine.show()
elif st.session_state.page == "diet":
    diet.show()
elif st.session_state.page == "dashboard":
    dashboard.show()
elif st.session_state.page == "history":
    history.show()
elif st.session_state.page == "report":
    report.show()
