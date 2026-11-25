from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from Utils.auth_guard import get_supabase_service

IST = ZoneInfo("Asia/Kolkata")


# Starting of the memory cleanup part
def prune_user_memories_by_time(
    user_email: str,
    keep_latest: int = 3,
    delete_from_source_tables: bool = True,
) -> dict:
    clean_email = (user_email or "").strip().lower()
    if not clean_email or keep_latest < 0:
        return {
            "kept": 0,
            "deleted_embeddings": 0,
            "deleted_user_data": 0,
            "deleted_journal": 0,
        }

    supabase = get_supabase_service()

    mem_res = (
        supabase.table("memory_embeddings")
        .select("id, created_at, source, text")
        .eq("user_email", clean_email)
        .order("created_at", desc=True)
        .execute()
    )
    memories = mem_res.data or []
    kept_memories = memories[:keep_latest]
    stale_memories = memories[keep_latest:]
    stale_ids = [m["id"] for m in stale_memories if m.get("id") is not None]

    deleted_embeddings = 0
    if stale_ids:
        supabase.table("memory_embeddings").delete().in_("id", stale_ids).execute()
        deleted_embeddings = len(stale_ids)

    deleted_user_data = 0
    deleted_journal = 0
    if delete_from_source_tables:
        ud_res = (
            supabase.table("user_data")
            .select("index, created_at")
            .eq("user_email", clean_email)
            .order("created_at", desc=True)
            .order("index", desc=True)
            .execute()
        )
        ud_rows = ud_res.data or []
        stale_ud_indices = [
            r["index"] for r in ud_rows[keep_latest:] if r.get("index") is not None
        ]
        if stale_ud_indices:
            supabase.table("user_data").delete().in_("index", stale_ud_indices).execute()
            deleted_user_data = len(stale_ud_indices)

        mj_res = (
            supabase.table("mood_journal")
            .select("id, created_at")
            .eq("user_email", clean_email)
            .order("created_at", desc=True)
            .order("id", desc=True)
            .execute()
        )
        mj_rows = mj_res.data or []
        stale_mj_ids = [
            r["id"] for r in mj_rows[keep_latest:] if r.get("id") is not None
        ]
        if stale_mj_ids:
            supabase.table("mood_journal").delete().in_("id", stale_mj_ids).execute()
            deleted_journal = len(stale_mj_ids)

    return {
        "kept": len(kept_memories),
        "deleted_embeddings": deleted_embeddings,
        "deleted_user_data": deleted_user_data,
        "deleted_journal": deleted_journal,
    }


def render_clean_memory_button(
    user_email: str,
    keep_latest: int = 3,
    label: str = "Cleanup",
    key: str = "clean_memory_btn",
) -> None:
    if st.button(label,  icon=":material/refresh:",key=key):
        with st.spinner("Cleaning old memories..."):
            try:
                prune_user_memories_by_time(
                    user_email=user_email,
                    keep_latest=keep_latest,
                )
                now_str = datetime.now(IST).strftime("%d %b %Y, %I:%M %p")
                st.session_state["last_clean_msg"] = (
                    f"Memory cleaned ({now_str}). Your {keep_latest} most recent memories are kept."
                )
                st.rerun()
            except Exception as e:
                st.session_state["last_clean_msg"] = f"Could not clean memories: {e}"