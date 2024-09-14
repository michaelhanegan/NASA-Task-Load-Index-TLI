import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def set_page_style():
    # Define custom CSS for light and dark modes
    light_mode_css = """
    <style>
        .stApp {
            background-color: #f5f5f5;
            color: #262730;
        }
        .stButton>button {
            color: #4F8BF9;
            border-color: #4F8BF9;
        }
        .stTextInput>div>div>input {
            color: #262730;
        }
        .project-context {
            background-color: white;
            border: 1px solid black;
            padding: 10px;
        }
        .stExpander {
            border: none !important;
        }
        .stExpander > div:first-child {
            border-radius: 0 !important;
            border: none !important;
        }
        .stExpander > div:last-child {
            border: none !important;
        }
    </style>
    """

    dark_mode_css = """
    <style>
        .stApp {
            background-color: #1e2130;
            color: #FAFAFA;
        }
        .stButton>button {
            color: #4F8BF9;
            border-color: #4F8BF9;
        }
        .stTextInput>div>div>input {
            color: #FAFAFA;
        }
        .project-context {
            background-color: #262730;
            border: 1px solid #4F8BF9;
            padding: 10px;
        }
        .stExpander {
            border: none !important;
        }
        .stExpander > div:first-child {
            border-radius: 0 !important;
            border: none !important;
        }
        .stExpander > div:last-child {
            border: none !important;
        }
    </style>
    """

    # Add fixed header bar with theme selection
    with stylable_container(
        key="header",
        css_styles="""
            {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 999;
                background-color: #262730;
                padding: 10px;
                display: flex;
                justify-content: flex-end;
            }
        """
    ):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            theme = st.radio(
                "Theme",
                ["🌞", "🌙", "💻"],
                horizontal=True,
                label_visibility="collapsed",
            )

    if theme == "🌞":
        st.markdown(light_mode_css, unsafe_allow_html=True)
    elif theme == "🌙":
        st.markdown(dark_mode_css, unsafe_allow_html=True)
    else:
        # System default (use Streamlit's default theme)
        pass

    # Add padding to the top of the page to account for the fixed header
    st.markdown(
        """
        <style>
        .main > div:first-child {
            padding-top: 60px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Improve accessibility and add plus/minus icons
    st.markdown("""
    <style>
    .stSlider>div>div>div>div {
        background-color: #4F8BF9 !important;
    }
    .stNumberInput>div>div>input {
        font-size: 1rem;
    }
    .slider-wrapper {
        display: flex;
        align-items: center;
    }
    .slider-icon {
        font-size: 1.5rem;
        margin: 0 10px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    return theme
