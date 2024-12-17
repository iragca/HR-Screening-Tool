import streamlit as st
import time

#importing the pages
from resume_screener import ResumeScreener
from user_documentation import UserDocumentation
from home import Home
from login import login

UserDocPage = st.Page(UserDocumentation, title="User Documentation", icon=":material/help:")
ResumeScreenerPage = st.Page(ResumeScreener, title="Resume Screener", icon=":material/recent_actors:")
HomePage = st.Page(Home, title="Home", icon=":material/home:")
LoginPage = st.Page(login, title="Login", icon=":material/login:")

if 'USER_DOC_PAGE' not in st.session_state:
    st.session_state.USER_DOC_PAGE = UserDocPage

if 'RESUME_SCREENER_PAGE' not in st.session_state:
    st.session_state.RESUME_SCREENER_PAGE = ResumeScreenerPage

if 'HOME_PAGE' not in st.session_state:
    st.session_state.HOME_PAGE = HomePage

if 'CURRENT_PAGE' not in st.session_state:
    st.session_state.CURRENT_PAGE = None

if "LOGGED_IN" not in st.session_state:
    st.session_state.LOGGED_IN = False

def logout():
    @st.dialog("Are you sure you want to log out?")

    def chose():
        col1, col2 = st.columns(spec=[1,1])

        with col1:
            if st.button("No", use_container_width=True):
                st.switch_page(st.session_state.CURRENT_PAGE)

        with col2:
            if st.button("Yes", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    chose()


logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

if st.session_state.LOGGED_IN:
    pages = {
        "Dashboard": [
            HomePage,
            ResumeScreenerPage,
        ],
        "Resources": [
            UserDocPage,
        ],
        "Account": [
            logout_page
        ]
    }

    pg = st.navigation(pages)
    pg.run()

else:
    login()
