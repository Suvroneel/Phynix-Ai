import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_service() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_KEY"],
    )


def require_google_auth():
    """Enforces Streamlit native Google login and populates session_state."""
    if not getattr(st.user, "is_logged_in", False):
        st.switch_page("Logout.py")

    email = (st.user.email or "").strip().lower()
    if not email:
        st.switch_page("Logout.py")

    st.session_state["logged_in"] = True
    st.session_state["user_email"] = email

    if not st.session_state.get("username"):
        supabase_service = get_supabase_service()
        res = (
            supabase_service.table("user_credentials")
            .select("user_name")
            .eq("email", email)
            .execute()
        )
        if res.data:
            st.session_state["username"] = res.data[0]["user_name"]
        else:
            st.switch_page("Logout.py")