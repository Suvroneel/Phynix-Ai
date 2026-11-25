import streamlit as st
from Utils.auth_guard import require_google_auth, get_supabase_service
from Utils.sidebar import render_sidebar_logo
from Utils.title import render_custom_header, render_custom_subheader
from Utils.disclaimer import render_notice
from Utils.toggle import render_clean_memory_button
from Utils.beta import render_header_with_beta
from Utils.memorycounter import render_memory_counter

# Authentication
require_google_auth()
supabase = get_supabase_service()
user_email = st.session_state["user_email"]
username = st.session_state["username"]

# Button CSS (matches 3_My Journals.py)
st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(90deg, #ff914d, #ff6e40);
            color: white !important;
            padding: 13px 10px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s ease;
            box-shadow: 0 4px 14px rgba(255, 110, 64, 0.3);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #ff6e40, #ff914d);
            box-shadow: 0 6px 18px rgba(255, 110, 64, 0.45);
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

render_sidebar_logo()

# ==========================================
# 1. MEMORY MANAGEMENT SECTION
# ==========================================
render_header_with_beta("Memory Management", badge_text="Beta")

render_memory_counter(
    user_email=user_email,
    label="Your Memories",

    table="memory_embeddings",
)

mem_left, mem_right = st.columns([4, 1], vertical_alignment="center")
with mem_left:
    render_notice(
        "Ashwa's response may get foggy if the memory keeps on piling.",
        font_size=16,
        color="#111111",
    )
with mem_right:
    render_clean_memory_button(
        user_email=user_email,
        keep_latest=3,
        label="Cleanup",
        key="clean_memory_btn",
    )

if st.session_state.get("last_clean_msg"):
    st.caption(st.session_state["last_clean_msg"])


# ==========================================
# 2. SETTINGS SECTION (Matches Ashva Diaries)
# ==========================================
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
render_custom_header("Settings")

col1, col2 = st.columns([4, 1], vertical_alignment="center")
with col1:
    render_custom_subheader("Logout of all sessions")
with col2:
    if st.button("Logout", type="tertiary", icon=":material/logout:"):
        st.session_state.clear()
        st.logout()