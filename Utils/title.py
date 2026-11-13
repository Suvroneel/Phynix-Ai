import streamlit as st
from datetime import datetime

def render_main_title():
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style='font-family:"Montserrat"; color:; font-size: 48px;'>
            Phynix_AI
        </h1>
    """, unsafe_allow_html=True)

#B22222
def render_tagline():

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
        <h3 style='font-family:"Poppins"; color:#B22222; font-size: 28px; font-weight: 400; margin-top:-15px;'>
            AI-Comapanion That Remembers You
        </h3>
    """, unsafe_allow_html=True)


def new_tagline():
    st.markdown("""
        <div style='font-size:14px; color:#777; text-align:center; margin-top: -10px;'>
            A gentle space to understand how you feel and support your emotional well-being.
        </div>
        """, unsafe_allow_html=True)

def render_full_header():
    render_main_title()
    render_tagline()


def render_welcome_message(username="User"):
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
        .custom-welcome {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            font-size: 25px;
            font-weight: 400;
            color: ;
            margin-bottom: 1rem;
            text-align: center; /* Added to center the text */
        }}
        </style>
        <div class="custom-welcome">Welcome, {username}</div>
        
        """,
        unsafe_allow_html=True
    )

def render_dynamic_greeting():
    current_time = datetime.now()
    hour = current_time.hour
    username = st.session_state.get("username", "friend")  # Default to "friend" if no username

    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:  # 02:01 PM IST falls here
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.markdown(f'<p style="text-align: center; font-family: Inter, sans-serif; font-size: 25px; font-weight: 400;">{greeting}, {username}</p>', unsafe_allow_html=True)


def render_custom_header(header_text):
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
            .streamlit-like-header {
                font-family: 'Inter', sans-serif;
                font-size: 30px;  /* Larger for stronger presence */
                font-weight: 500;
                color: var(--text-color);
                margin-bottom: -8px;  /* Pull divider closer */
                margin-top: 32px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="streamlit-like-header">{header_text}</div>', unsafe_allow_html=True)

    # Default Streamlit divider
    st.divider()



def render_custom_header2(header_text):
    st.markdown("""
        <style>
            .ashva-divider {
                font-family: 'Inter', sans-serif;
                font-size: 30px;
                font-weight: 500;
                color: var(--text-color);
                margin-bottom: -8px;
                margin-top: 0px;
                padding-top: 0px;
            }
        </style>
    """, unsafe_allow_html=True)


    st.divider()

def render_custom_subheader(header_text):
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
            .streamlit-like-subheader {
                font-family: 'Inter', sans-serif;
                font-size: 24px;  /* Larger for stronger presence */
                font-weight: 500;
                color: var(--text-color);
                
                margin-top: -30px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="streamlit-like-subheader">{header_text}</div>', unsafe_allow_html=True)

    # Default Streamlit divider


#testing



