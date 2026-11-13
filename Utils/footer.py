import streamlit as st

def render_footer():
    """
    Renders the custom footer for the Streamlit app.
    """
    st.markdown("""
       <style>
    /* General Footer Styling */
    .footer {
    position: fixed; 
       bottom: 0;  
        left: 0;
        width: 100%;
        background-color: #1A2526; /* Dark teal-gray for tech vibe */
        color: #F5F6F5; /* Soft off-white */
        text-align: center;
        padding: 12px 20px;
        font-family: 'Inter', 'Roboto', 'Helvetica', 'Arial', sans-serif;
        font-size: 14.5px;
        z-index: 10000;
        box-shadow: 0 -1px 2px rgba(0, 0, 0, 0.06);
    }

    /* Link Styling */
    .footer a {
        color: #B22222; /* Project Phynix red */
        text-decoration: none;
        transition: color 0.3s ease, transform 0.3s ease;
        margin: 0 8px;
        letter-spacing: 0.2px;
    }

    .footer a:hover {
        color: #D97C7C; /* Lighter red */
        transform: scale(1.05);
        text-decoration: underline;
    }

    /* Separator Styling */
    .footer .separator {
        color: #627677; /* Muted teal-gray */
        margin: 0 5px;
    }

    /* Copyright and Tagline Styling */
    .footer p {
        margin: 6px 0 0;
        line-height: 1.5;
        color: #A8B5B7;
        font-size: 12.5px;
    }

    .footer .tagline {
        color: #A8B5B7;
        font-size: 12.5px;
        margin: 4px 0 0;
        font-style: italic;
    }

    /* Made by Section Styling */
    .footer .made-by-section {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        margin-bottom: 4px;
    }

    /* Highlight Name and Project Phynix */
    .footer .name, .footer .project {
        font-weight: 600;
        letter-spacing: 0.2px;
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<div class="footer">
    <div class="made-by-section">
        <span>Made by</span>
        <a href="https://www.linkedin.com/in/suvroneel-nathak-593602197/" target="_blank" class="name">Suvroneel Nathak</a>
        <span class="separator">|</span>
        <a href="https://github.com/Suvroneel" target="_blank">GitHub</a>
        <span class="separator">|</span>
        <a href="https://github.com/Suvroneel" target="_blank">Contact</a>
    </div>
    <p>© 2025 <span class="project">Project Phynix</span></p>
    
</div>
    """, unsafe_allow_html=True)
