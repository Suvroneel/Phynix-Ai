import streamlit as st


def render_notice(text: str, font_size: int = 16, color: str = "#111111", line_break_after: str | None = None):
    """
    Renders a plain, unboxed text notice with configurable text, font size,
    color, and optional line break right after a specified substring.
    """
    formatted_text = text
    if line_break_after and line_break_after in formatted_text:
        formatted_text = formatted_text.replace(
            line_break_after, f"{line_break_after}<br>", 1
        )

    st.markdown(
        f"""
        <p style="
            font-family: 'Inter', sans-serif;
            font-size: {font_size}px;
            line-height: 1.5;
            color: {color};
            margin: 8px 0 18px 0;
        ">
            {formatted_text}
        </p>
        """,
        unsafe_allow_html=True,
    )