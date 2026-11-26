from datetime import datetime
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from Utils.auth_guard import get_supabase_service
from Utils.title import render_custom_subheader


def render__status(header_text):
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap" rel="stylesheet">
        <style>
            .status{
                font-family: 'Inter', sans-serif;
                font-size: 18px;  /* Larger for stronger presence */
                font-weight: 500;
                color: var(--text-color);

                margin-top: -30px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="status">{header_text}</div>', unsafe_allow_html=True)


# risks
def show_last_chat_metrics(user_name: str):
    supabase = get_supabase_service()
    render_custom_subheader("Mental Metrics Summary")
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    response = supabase.table("user_data") \
        .select("created_at, risks") \
        .eq("user_name", user_name) \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute()

    if not response.data or len(response.data) < 2:
        st.warning("Not enough chat entries to compare.")
        return

    df = pd.DataFrame(response.data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["risks"] = df["risks"].str.strip().str.lower()

    risk_map = {"low": 10, "moderate": 50, "neutral": 10, "high": 90}
    df["risk_val"] = df["risks"].map(risk_map)

    # Reverse order: oldest first
    df = df.sort_values("created_at")

    half = len(df) // 2
    prev_chunk = df.iloc[:half]
    current_chunk = df.iloc[half:]

    prev_risk = prev_chunk["risk_val"].mean()
    current_risk = current_chunk["risk_val"].mean()

    current_confidence = 100 - current_risk
    prev_confidence = 100 - prev_risk

    current_mental = min(100, (current_confidence + (100 - current_risk) / 2))
    prev_mental = min(100, (prev_confidence + (100 - prev_risk) / 2))

    def inline_percent_change(current, previous):
        try:
            current = float(current)
            previous = float(previous)
            if previous == 0:
                return "N/A"
            change = ((current - previous) / abs(previous)) * 100

            # Limit change between -98 and +98
            change = max(min(change, 98), -98)

            sign = "+" if change > 0 else "-"
            return f"{sign}{abs(change):.2f}%"
        except:
            return "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("Confidence", f"{current_confidence:.0f}%", inline_percent_change(current_confidence, prev_confidence),
                delta_color="normal")
    col2.metric("Risk", f"{current_risk:.0f}%", inline_percent_change(current_risk, prev_risk), delta_color="inverse")
    col3.metric("Mental Health", f"{current_mental:.0f}%", inline_percent_change(current_mental, prev_mental),
                delta_color="normal")

    if current_mental >= 70:
        status = " Stable ✔"
        color = "green"
    elif current_mental >= 60:
        status = " Caution ❗"
        color = "Orange"
    else:
        status = " Vulnerable ⚠"
        color = "red"

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-weight: 500; font-size: 20px;'>Status: <span style='color:{color};'>{status}</span></p>",
        unsafe_allow_html=True
    )


def session_progress(user_name: str):
    supabase = get_supabase_service()
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    render_custom_subheader("Emotion Snapshot – Today")
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    today = datetime.now().date()

    response = supabase.table("user_data") \
        .select("created_at, predicted_emotion") \
        .eq("user_name", user_name) \
        .execute()

    if not response.data:
        st.warning("No emotion data found.")
        return

    df = pd.DataFrame(response.data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date_only"] = df["created_at"].dt.date
    df["time_only"] = df["created_at"].dt.strftime("%I:%M %p")

    df = df[df["date_only"] == today]

    emotion_levels = {
        "joy": 6, "surprise": 5, "neutral": 4,
        "disgust": 3, "sadness": 2, "fear": 1, "anger": 0
    }

    if df.empty:
        dummy_df = pd.DataFrame({
            "created_at": [datetime.now()],
            "emotion_val": [0],
            "time_only": ["--"],
            "predicted_emotion": ["none"]
        })

        chart = alt.Chart(dummy_df).mark_bar(size=35).encode(
            x=alt.X("created_at:T", title="Time of Day",
                    axis=alt.Axis(format="%I:%M %p", grid=False, domain=True, values=[])),
            y=alt.Y("emotion_val:Q",
                    scale=alt.Scale(domain=[0, 6]),
                    axis=alt.Axis(
                        labels=False, ticks=False, domain=False, grid=False
                    )),
            color=alt.value("#047857"),
            tooltip=["time_only:N", "predicted_emotion:N"]
        ).properties(title="Today’s Emotion Flow")

        st.altair_chart(chart, use_container_width=True)
        st.info("No entries recorded yet today.")
        return

    df["predicted_emotion"] = df["predicted_emotion"].str.lower().str.strip()
    df = df[df["predicted_emotion"].isin(emotion_levels)]
    df["emotion_val"] = df["predicted_emotion"].map(emotion_levels)
    df = df.sort_values("created_at")

    # Get only first and last actual timestamps
    first_time = df["created_at"].iloc[0]
    last_time = df["created_at"].iloc[-1]

    chart = alt.Chart(df).mark_bar(size=35).encode(
        x=alt.X("created_at:T",
                title="Time of Day",
                axis=alt.Axis(
                    format="%I:%M %p",
                    grid=False,
                    domain=True,
                    values=[first_time, last_time],
                    labelAngle=0
                )),
        y=alt.Y("emotion_val:Q",
                scale=alt.Scale(domain=[0, 6]),
                axis=alt.Axis(
                    labels=False, ticks=False, domain=False, grid=False
                )),
        color=alt.value("#047857"),
        tooltip=["time_only:N", "predicted_emotion:N"]
    ).properties(title="Today’s Emotion Flow")

    st.altair_chart(chart, use_container_width=True)


def session_progress2(user_name: str):
    supabase = get_supabase_service()
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    render_custom_subheader("Emotion Progress")
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    response = supabase.table("user_data") \
        .select("created_at, predicted_emotion") \
        .eq("user_name", user_name) \
        .order("created_at", desc=True) \
        .limit(7) \
        .execute()

    if not response.data or len(response.data) < 2:
        st.warning("Not enough emotion data to show progress.")
        return

    df = pd.DataFrame(response.data)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["predicted_emotion"] = df["predicted_emotion"].str.strip().str.lower()

    # Emotion mapping (Joy at the top)
    emotion_levels = {
        "joy": 6,
        "surprise": 5,
        "neutral": 4,
        "disgust": 3,
        "sadness": 2,
        "fear": 1,
        "anger": 0
    }

    df = df[df["predicted_emotion"].isin(emotion_levels.keys())]
    df["emotion_val"] = df["predicted_emotion"].map(emotion_levels)
    df = df.sort_values("created_at")

    # Line histogram: bars + line overlay
    bars = alt.Chart(df).mark_bar(size=20).encode(
        x=alt.X("created_at:T", title="Date"),
        y=alt.Y("emotion_val:Q",
                title="Emotion",
                scale=alt.Scale(domain=[0, 6]),
                axis=alt.Axis(
                    values=list(emotion_levels.values()),
                    labelExpr="{0: 'anger', 1: 'fear', 2: 'sadness', 3: 'disgust', 4: 'neutral', 5: 'surprise', 6: 'joy'}[datum.value]"
                )),
        color=alt.value("#3b82f6"),  # Tailwind blue-500
        tooltip=["created_at", "predicted_emotion"]
    )

    line = alt.Chart(df).mark_line(point=True, interpolate='monotone', stroke="#111827").encode(
        x="created_at:T",
        y="emotion_val:Q"
    )

    chart = (bars + line).properties(
        title="Emotion Trend (Histogram + Line)"
    )

    st.altair_chart(chart, use_container_width=True)

    # Status label based on average emotion
    avg_emotion = df["emotion_val"].mean()

    if avg_emotion >= 5:
        status = "Stable ✅"
        color = "green"
    elif avg_emotion >= 3.5:
        status = "Mixed ⚖️"
        color = "orange"
    else:
        status = "Downshift ⚠"
        color = "red"

    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-weight: 500; font-size: 20px;'>Status: <span style='color:{color};'>{status}</span></p>",
        unsafe_allow_html=True
    )
