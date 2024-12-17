import streamlit as st
from streamlit_lottie import st_lottie

from user_documentation import UserDocumentation
from resume_screener import ResumeScreener

def Home():

    st.session_state.CURRENT_PAGE = st.session_state.HOME_PAGE

    st.set_page_config(
        page_title="HR Resume Screener",
        page_icon="🏠",
        layout="centered",
        initial_sidebar_state="auto"
    )

    st.title("Resume Screener Tool")
    st_lottie(
        "https://lottie.host/c9d629b5-3b69-4e54-9d63-6e21c16d0c04/UYSzseW0Rv.json",
        loop=False,
        height=200,
        width=400,
        )
    st.write("If you are new to using this tool, " + \
        "you can read the User Documentation as a guide.")

    st.page_link(
        st.Page(UserDocumentation, title="User Documentation"), 
        label="User Documentation", 
        icon="📃"
        )

    st.write("Or you can start screening right away.")

    st.page_link(
        st.Page(ResumeScreener, title="Resume Screener"), 
        label="Resume Screener", 
        icon="🔎"
        )
