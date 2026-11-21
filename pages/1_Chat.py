import streamlit as st
import postgrest.exceptions
from Utils.auth_guard import require_google_auth, get_supabase_service
from Utils.ashva import display_welcome_message
from Utils.model import predict_emotion
from Utils.emotion_responses import get_risk_with_emoji
from Utils.gen_ai import PhynixAI
from Utils.sidebar import render_sidebar_logo
from Utils.title import render_main_title, render_dynamic_greeting, new_tagline
from Utils.memory import upsert_memory

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">

    <style>
    body, .bubble, .user-bubble {
        font-family: 'Inter', sans-serif !important;
    }
    .bubble {
        position: relative;
        background-color: #f9f9f9;
        padding: 14px 18px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: #444;
        max-width: 600px;
        display: inline-block;
        line-height: 1.5;
        margin-top: 16px;
    }

    .bubble::before {
        content: "";
        position: absolute;
        top: 18px;
        left: -10px;
        width: 0;
        height: 0;
        border-top: 10px solid transparent;
        border-bottom: 10px solid transparent;
    }

    .ashva-reply {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .ashva-reply img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
    }

    .user-reply {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-top: 16px;
    }

    .user-bubble {
        background-color: #f9f9f9;
        padding: 14px 18px;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        color: #444;
        line-height: 1.5;
        max-width: 600px;
        display: inline-block;
        border: 1px solid #eeeeee;
    }

    details summary {
        cursor: pointer;
        font-size: 15px;
        color: #444;
    }

    details[open] summary {
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication
require_google_auth()
supabase = get_supabase_service()
user_email = st.session_state["user_email"]
username = st.session_state["username"]

# Check if returning user
user_history_check = (
    supabase.table("user_data")
    .select("index")
    .eq("user_email", user_email)
    .neq("messages", "Initial message")
    .execute()
)
is_returning_user = len(user_history_check.data) > 0

render_sidebar_logo()

# Initialize GenAI
if "phynix_ai" not in st.session_state:
    st.session_state.phynix_ai = PhynixAI()

# Init messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "message_submitted" not in st.session_state:
    st.session_state.message_submitted = False


st.markdown("""
    <style>
        .st-emotion-cache-yinll1 { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Top controls
col_one, col_two = st.columns([4, 1])
with col_two:
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

    new_chat = st.button("New chat", icon=":material/stylus_laser_pointer:", use_container_width=True)

if new_chat:
    st.session_state.messages = []
    st.session_state.message_submitted = False
    st.rerun()

col1, col2 = st.columns([1, 4])
with col1:
    st.image("images/sigmund-ljJDx95-6gE-unsplash.png", use_container_width=True, width=100)
with col2:
    render_main_title()

new_tagline()

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

if not is_returning_user and len(st.session_state.messages) == 0:
    st.session_state.messages = []
    st.session_state.message_submitted = False
    render_dynamic_greeting()
    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 8px; font-size: 13px; color: #0000FF;'>
            ✨A brand new chapter, You_AI, is in active development right now ✨
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='font-family: Inter, sans-serif; font-size:16px; color:#666; margin-top:20px; text-align: center;'>
            Welcome to <strong>Phynix</strong> — a space to reflect and share what you're feeling.<br>
            You can talk about your day, your thoughts, or anything that's been on your mind.<br>
            I'm <strong>Ashva</strong>, your companion inside Phynix — here to listen, understand your emotional state, and support you gently.
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div style='font-family: Inter, sans-serif; font-size:15px; color: #666; margin-top: 20px; margin-bottom: 10px; text-align:center;'>
            ✨ Not sure where to start? Try one of these:<br>
            • "Today, I'm feeling..."<br>
            • "Lately, what's been bothering me is..."<br>
            • "Something that made me smile today was..."
        </div>
    """, unsafe_allow_html=True)

elif len(st.session_state.messages) == 0:
    render_dynamic_greeting()
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    display_welcome_message(username, user_email)

# Model selector - ABOVE chat input
col_model1, col_model2 = st.columns([4, 1])

with col_model2:
    model_info = st.session_state.phynix_ai.get_model_info()
    current_model_key = [
        k for k, v in st.session_state.phynix_ai.available_models.items()
        if v == model_info["current"]
    ][0]

    selected_model = st.selectbox(
        "Select AI Model",
        options=model_info["available"],
        index=model_info["available"].index(current_model_key),
        key="model_selector",
    )

    if st.session_state.phynix_ai.available_models[selected_model] != model_info["current"]:
        st.session_state.phynix_ai.set_model(selected_model)
        st.rerun()

# Chat input
prompt = st.chat_input("How are you feeling today?")

if prompt:
    emotion_label = predict_emotion(prompt)
    risk_level = get_risk_with_emoji(emotion_label)

    chat_history = []
    for msg in st.session_state.messages:
        chat_history.append({
            "role": msg["sender"] if msg["sender"] == "user" else "assistant",
            "content": (
                msg["content"]
                if msg["sender"] == "user"
                else msg["content"].split("<details>")[0].strip()
            ),
        })

    with st.spinner("Ashva is thinking..."):
        ai_reply = st.session_state.phynix_ai.generate_response(
            user_message=prompt,
            detected_emotion=emotion_label,
            risk_level=risk_level,
            chat_history=chat_history,
            max_tokens=300,
            temperature=0.7,
        )

    try:
        response = (
            supabase.table("user_credentials")
            .select("user_name, email")
            .eq("email", user_email)
            .execute()
        )
        if not response.data:
            supabase.table("user_credentials").insert({
                "user_name": username,
                "email": user_email,
            }).execute()

        count_response = (
            supabase.table("user_data")
            .select("index", count="exact")
            .execute()
        )
        next_id = (count_response.count or 0) + 1

        supabase.table("user_data").insert({
            "index": next_id,
            "user_email": user_email,
            "user_name": username,
            "messages": prompt,
            "predicted_emotion": emotion_label,
            "risks": risk_level,
            "replies": ai_reply,
        }).execute()

        upsert_memory(
            record_id=f"chat_{next_id}",
            text=prompt,
            user_email=user_email,
            user_name=username,
            source="chat",
        )

    except postgrest.exceptions.APIError as e:
        st.error(f"Failed to save data: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.stop()

    st.session_state.messages.append({
        "sender": "user",
        "content": prompt,
    })

    analysis_block = f"""
<details>
  <summary style='font-weight: normal; color: #444;'>Analysis</summary>
  <div style='margin-top: 10px;'>
    Here's my analysis for you:<br>
    <div style='margin-top: 10px;'>
      <strong>Emotion:</strong> {emotion_label.capitalize()}<br>
      <div style='margin-top: 5px;'>
        <strong>Risk Level:</strong> {risk_level.capitalize()}
      </div>
    </div>
  </div>
</details>
"""

    st.session_state.messages.append({
        "sender": "bot",
        "content": f"{ai_reply}<br><br>{analysis_block}",
    })

    st.session_state.message_submitted = True

# Display messages
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f"""
        <div class="user-reply">
            <div class="user-bubble">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ashva-reply">
            <img src="https://images.unsplash.com/vector-1741104195197-893ea9e09a37?q=80&w=939&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Ashva">
            <div class="bubble">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)