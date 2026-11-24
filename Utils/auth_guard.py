import streamlit as st
from supabase import Client, create_client


@st.cache_resource(show_spinner=False)
def get_supabase_service() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SERVICE_KEY"],
    )


def get_supabase_anon() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


def _load_username_for_email(email: str) -> str | None:
    supabase_service = get_supabase_service()
    res = (
        supabase_service.table("user_credentials")
        .select("user_name")
        .eq("email", email)
        .execute()
    )
    if res.data:
        return res.data[0]["user_name"]
    return None


def restore_supabase_session() -> bool:
    """
    Restores a Supabase session from st.session_state or URL query params
    so the user stays logged in across refreshes and redeploys.
    """
    if st.session_state.get("logged_in") and st.session_state.get("user_email"):
        return True

    access_token = st.session_state.get("access_token") or st.query_params.get("sb_at")
    refresh_token = st.session_state.get("refresh_token") or st.query_params.get("sb_rt")

    if not access_token or not refresh_token:
        return False

    try:
        supabase = get_supabase_anon()
        session_res = supabase.auth.set_session(access_token, refresh_token)
        user = session_res.user if session_res else None
        if not user or not user.email:
            return False

        email = user.email.strip().lower()
        new_at = session_res.session.access_token if session_res.session else access_token
        new_rt = session_res.session.refresh_token if session_res.session else refresh_token

        st.session_state["access_token"] = new_at
        st.session_state["refresh_token"] = new_rt
        st.session_state["user_email"] = email
        st.session_state["logged_in"] = True

        st.query_params["sb_at"] = new_at
        st.query_params["sb_rt"] = new_rt

        username = _load_username_for_email(email)
        if username:
            st.session_state["username"] = username

        return True
    except Exception:
        return False


def require_google_auth():
    """Enforces authenticated session and populates session_state."""
    if not restore_supabase_session():
        st.switch_page("Logout.py")

    email = (st.session_state.get("user_email") or "").strip().lower()
    if not email:
        st.switch_page("Logout.py")

    if not st.session_state.get("username"):
        username = _load_username_for_email(email)
        if username:
            st.session_state["username"] = username
        else:
            st.switch_page("Logout.py")


def logout_user():
    """Logs out of Supabase session, clears session state and URL tokens."""
    try:
        access_token = st.session_state.get("access_token")
        refresh_token = st.session_state.get("refresh_token")
        supabase = get_supabase_anon()
        if access_token and refresh_token:
            supabase.auth.set_session(access_token, refresh_token)
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.clear()
    for key in ["sb_at", "sb_rt", "code"]:
        if key in st.query_params:
            del st.query_params[key]
    st.switch_page("Logout.py")
