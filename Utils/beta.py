import streamlit as st
from Utils.title import render_custom_header


def render_header_with_beta(
    title: str,
    badge_text: str = "Beta",
    color: str = "green",
) -> None:
    """
    Renders a section header with Streamlit's native st.badge pill
    matching the Verified badge style without a checkmark.
    """
    title_col, badge_col = st.columns([5, 1], vertical_alignment="center")
    with title_col:
        render_custom_header(title)
    with badge_col:
        st.badge(badge_text, color=color)