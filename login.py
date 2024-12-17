import streamlit as st
from home import Home

def login():

    st.set_page_config(
        page_title="Login Page",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    col1, col2, col3 = st.columns(spec=[1, 3, 1])

    with col2:
        st.title("Login")
        username = st.text_input("Email Address", value='johndoe@hr.company.com')
        password = st.text_input("Password", type="password")


        col1, col2 = st.columns(spec=[1,1])

        with col1:
            if st.button(
                label="Forgot Password?", 
                use_container_width=True,
                type="secondary"
                ):

                st.info("Please contact your manager or the IT department for a password reset.")

        with col2:
            if st.button(
                label="Login", 
                use_container_width=True,
                type="primary"
                ):

                class UnregisteredUser(Exception):
                    """
                    Represents an exception when the user is not registered.
                    """

                    def __init__(self, message="User not registered"):
                        self.message = message
                        super().__init__(self.message)

                class IncompleteDetails(Exception):
                    """
                    Represents an exception when the user's details are incomplete.
                    """

                    def __init__(self, message="Incomplete details"):
                        self.message = message
                        super().__init__(self.message)

                #imaginary db calls for existing user, if user is in imaginary db, user is logged in
                try:
                    if username == "johndoe@hr.company.com" and password == "password":
                        st.session_state.LOGGED_IN = True
                        st.switch_page(st.Page(Home, title="Home", icon=":material/home:"))

                    if username == "" or password == "":
                        raise IncompleteDetails

                    raise UnregisteredUser

                except UnregisteredUser as e:
                    st.error(e)
                except IncompleteDetails as e:
                    st.error(e)