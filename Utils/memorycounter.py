import streamlit as st
from Utils.auth_guard import get_supabase_service


def get_memory_count(user_email: str, table: str = "memory_embeddings") -> int:
    clean_email = (user_email or "").strip().lower()
    if not clean_email:
        return 0

    supabase = get_supabase_service()
    res = (
        supabase.table(table)
        .select("id", count="exact")
        .eq("user_email", clean_email)
        .execute()
    )
    if getattr(res, "count", None) is not None:
        return int(res.count)
    return len(res.data or [])


def render_memory_counter(
    user_email: str,
    label: str = "Your Memories",
    table: str = "memory_embeddings",
) -> int:
    count = get_memory_count(user_email=user_email, table=table)

    st.markdown(
        f"""
        <div style="margin: 8px 0 14px 0;">
            <div style="
                font-size: 18px;
                font-weight: 600;
                color: #ff6e40;
                margin-bottom: 4px;
            ">{label}</div>
            <div style="
                font-size: 40px;
                font-weight: 700;
                color: #111111;
                line-height: 1.1;
                letter-spacing: -0.5px;
            ">{count}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return count