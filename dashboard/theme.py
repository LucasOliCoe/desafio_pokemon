import streamlit as st

def pokedex_css():
    """
    Injeta CSS global nas páginas.
    """
    CSS = """
    <style>
    .pokedex-box {
        background: #1e293b;
        border: 2px solid #facc15;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    .pokedex-title {
        color: #facc15;
        font-weight: 800;
        font-size: 28px;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 10px;
    }

    .pokedex-subtitle {
        color: #e5e7eb;
        font-size: 16px;
        margin-bottom: 10px;
    }
    </style>
    """
    st.markdown(CSS, unsafe_allow_html=True)
