import re
import streamlit as st
from Utils.auth_guard import get_supabase_service
from Utils.footer import render_footer
from Utils.sidebar import hide_sidebar, add_sidebar_tooltip
from Utils.title import render_main_title, render_tagline

st.set_page_config(
    page_title="Phynix_AI",
    page_icon="images/icons/favicon.ico",
    initial_sidebar_state="collapsed",
)

hide_sidebar()
add_sidebar_tooltip()

supabase_service = get_supabase_service()


@st.dialog("Welcome to Phynix")
def setup_username_dialog(user_email: str):
    st.write(f"Signed in as **{user_email}**")
    st.write("Choose a display username to get started:")

    suggested = re.sub(r"[^a-zA-Z0-9_]", "", user_email.split("@")[0]) or "friend"
    new_username = st.text_input(
        "Username (no spaces)",
        value=suggested,
        key="google_username_dialog",
    )

    if st.button("Continue to Phynix", use_container_width=True, type="primary"):
        clean_name = new_username.strip()
        if not clean_name:
            st.error("Please enter a username.")
        elif re.search(r"\s", clean_name):
            st.error("Username cannot contain spaces.")
        else:
            try:
                count_res = (
                    supabase_service.table("user_credentials")
                    .select("user_id", count="exact")
                    .execute()
                )
                new_user_id = (count_res.count or 0) + 1

                supabase_service.table("user_credentials").insert({
                    "user_id": new_user_id,
                    "email": user_email,
                    "user_name": clean_name,
                }).execute()

                st.session_state["username"] = clean_name
                st.session_state["user_email"] = user_email
                st.session_state["logged_in"] = True
                st.switch_page("pages/1_Chat.py")
            except Exception as e:
                st.error(f"Could not create profile: {e}")


# Handle active Google OAuth session
if getattr(st.user, "is_logged_in", False):
    user_email = (st.user.email or "").strip().lower()
    if user_email:
        st.session_state["user_email"] = user_email
        st.session_state["logged_in"] = True

        try:
            existing = (
                supabase_service.table("user_credentials")
                .select("user_name")
                .eq("email", user_email)
                .execute()
            )
            if existing.data:
                st.session_state["username"] = existing.data[0]["user_name"]
                st.switch_page("pages/1_Chat.py")
            else:
                setup_username_dialog(user_email)
        except Exception as e:
            st.error(f"Database connection error: {e}")

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("images/sigmund-ljJDx95-6gE-unsplash.png", use_container_width=True, width=100)
with col2:
    render_main_title()
    render_tagline()

st.markdown("""
    <style>
        .st-emotion-cache-yinll1 { display: none !important; }
        .login-card {
            max-width: 440px;
            margin: 48px auto 24px auto;
            padding: 32px 28px;
            border-radius: 14px;
            border: 1px solid #f0e6df;
            background: #ffffff;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.05);
            text-align: center;
            font-family: 'Inter', sans-serif;
        }
        .login-card h3 {
            margin: 0 0 8px 0;
            font-weight: 600;
            color: #222;
        }
        .login-card p {
            margin: 0 0 22px 0;
            font-size: 14px;
            color: #666;
            line-height: 1.5;
        }
        .stButton > button {
            background: linear-gradient(90deg, #ff914d, #ff6e40);
            color: white !important;
            border: none;
            border-radius: 10px;
            padding: 12px 18px;
            font-weight: 600;
            font-size: 15px;
            box-shadow: 0 4px 14px rgba(255, 110, 64, 0.3);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #ff6e40, #ff914d);
            color: white !important;
        }
    </style>
    <div class="login-card">
        <h3>Welcome to Phynix</h3>
        <p>Sign in with your Google account to continue your conversations, memory, and daily reflections with Ashva.</p>
    </div>
""", unsafe_allow_html=True)

_, center_col, _ = st.columns([1.2, 2, 1.2])
with center_col:
    if st.button("Continue with Google", use_container_width=True):
        st.login("google")

st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)
render_footer()