import streamlit as st
from sentence_transformers import SentenceTransformer
from Utils.auth_guard import get_supabase_service


@st.cache_resource
def get_supabase():
    return get_supabase_service()


@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str):
    embedder = load_embedder()
    return embedder.encode(text).tolist()


def upsert_memory(record_id: str, text: str, user_email: str, user_name: str, source: str):
    vector = embed_text(text)
    supabase = get_supabase()

    supabase.table("memory_embeddings").upsert({
        "id": record_id,
        "user_email": user_email,
        "user_name": user_name,
        "source": source,
        "text": text,
        "embedding": vector
    }).execute()


def retrieve_memories(query: str, user_email: str, top_k: int = 4):
    vector = embed_text(query)
    supabase = get_supabase()

    response = supabase.rpc("match_memories", {
        "query_embedding": vector,
        "match_user_email": user_email,
        "match_count": top_k
    }).execute()

    return response.data
