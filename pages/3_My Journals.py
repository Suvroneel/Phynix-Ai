from datetime import datetime
from zoneinfo import ZoneInfo
import random
import uuid
import streamlit as st
from Utils.auth_guard import require_google_auth, get_supabase_service
from Utils.journal import fetch_today_entries, insert_entry, upload_image
from Utils.profile import prof_change, profile_name
from Utils.sidebar import render_sidebar_logo
from Utils.title import render_custom_header2, render_custom_subheader
from Utils.ashva import ashva_diary
from Utils.memory import upsert_memory

IST = ZoneInfo("Asia/Kolkata")

# Authentication
require_google_auth()
supabase = get_supabase_service()

# Button CSS
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

# Custom CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem !important;
    }
    .stImage > img {
        max-width: 100%;
        max-height: 400px;
        width: 100%;
        object-fit: cover;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .custom-welcome {
        margin-bottom: 0 !important;
        line-height: 1.15 !important;
    }
    </style>
""", unsafe_allow_html=True)

render_sidebar_logo()

# Initialize session state
if "profile_image" not in st.session_state:
    st.session_state.profile_image = "images/profiles/profile1.png"

if "journal_input_key" not in st.session_state:
    st.session_state.journal_input_key = 0

if "show_entries" not in st.session_state:
    st.session_state.show_entries = True

# Page title & subheader
st.markdown(
    "<h1 style='font-family:\"Montserrat\"; font-size: 42px; margin-bottom: 4px;'>My Journals</h1>",
    unsafe_allow_html=True,
)
render_custom_subheader("Some thoughts don't need an answer.")

# Space between subheader and profile block
st.markdown("<div style='margin-top: 26px;'></div>", unsafe_allow_html=True)

# Profile picture
st.image(st.session_state.profile_image, width=200)
st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

# Username row with Edit Profile right beside it
name_col, edit_col = st.columns([4, 1], vertical_alignment="center")
with name_col:
    profile_name(st.session_state["username"])
with edit_col:
    if st.button("Edit Profile", icon=":material/draw:", key="edit_profile_btn", use_container_width=True):
        prof_change()

st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
badge = st.badge("Verified ✔", color="green")

st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)

entry_text = st.text_area(
    "entry",
    placeholder=random.choice(ashva_diary),
    height=180,
    max_chars=2000,
    label_visibility="collapsed",
    key=f"journal_text_{st.session_state.journal_input_key}",
)

uploaded_file = st.file_uploader(
    "Add a photo (optional)",
    type=["jpg", "jpeg", "png", "webp"],
    key=f"journal_image_{st.session_state.journal_input_key}",
)

colA, colB = st.columns([4, 1])
with colB:
    if st.button("Upload", icon=":material/draw:", key="upload_btn", use_container_width=True):
        if entry_text.strip():
            image_url = (
                upload_image(st.session_state["username"], uploaded_file)
                if uploaded_file
                else None
            )
            insert_entry(
                st.session_state["username"],
                st.session_state["user_email"],
                entry_text.strip(),
                image_url,
            )

            upsert_memory(
                record_id=f"diary_{uuid.uuid4().hex}",
                text=entry_text.strip(),
                user_email=st.session_state["user_email"],
                user_name=st.session_state["username"],
                source="diary",
            )

            st.session_state.journal_input_key += 1
            st.session_state.show_entries = True
            st.rerun()
        else:
            st.warning("Write something first.")

render_custom_header2("")

colabc, colxyz = st.columns([4, 1])
with colxyz:
    if st.button("Clear", icon=":material/refresh:", type="tertiary", key="clear_btn"):
        st.session_state.show_entries = False
        st.rerun()

if st.session_state.show_entries:
    for entry in fetch_today_entries(st.session_state["username"]):
        try:
            dt = (
                datetime.fromisoformat(entry["created_at"])
                .astimezone(IST)
                .strftime("%d %b %Y, %I:%M %p")
            )
        except Exception:
            dt = entry["created_at"]

        image_html = (
            f'<img src="{entry["image_url"]}" style="width:100%; border-radius:8px; margin-top:12px; object-fit:contain; max-height:300px;">'
            if entry.get("image_url")
            else ""
        )

        st.markdown(f"""
            <div style="
                border-left: 3px solid #ff914d;
                border-radius: 4px;
                padding: 18px 20px;
                margin-bottom: 16px;
                font-family: 'Inter', sans-serif;
            ">
                <p style="color:#ff914d; font-size:11px; margin:0 0 10px 0;">{dt}</p>
                <p style="font-size:15px; line-height:1.7; margin:0;">{entry['entry']}</p>
                {image_html}
            </div>
        """, unsafe_allow_html=True)