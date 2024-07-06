from typing import Callable, Tuple

import streamlit as st

from src.definitions.constants import LOGIN_BUTTON, LOGIN_SCREEN, REGISTER_BUTTON, REGISTER_SCREEN
from src.definitions.messages import Messages
from src.services.server import server
from src.utils.decorators import authentication


class Authentication:
    def __init__(self):
        self.server = server

    @authentication(success_msg=Messages.login_success_message(), fail_msg=Messages.login_failed_message())
    def _login(self, username: str, password: str) -> Tuple[bool, str]:
        return self.server.login_user(username=username, password=password)

    @authentication(success_msg=Messages.register_success_message(), fail_msg=Messages.register_failed_message())
    def _register(self, name: str, username: str, password: str) -> Tuple[bool, str]:
        return self.server.register_user(name=name, username=username, password=password)

    """ 
    Screens
    """
    def login_screen(self, callback: Callable):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button(LOGIN_BUTTON):
            if st.session_state.screen == LOGIN_SCREEN:
                st.session_state.logged_in, name = self._login(username=username, password=password)
                if st.session_state.logged_in:
                    st.session_state.user = username
                    st.session_state.name = name if name != "" else username
                    callback()
                    st.rerun()

        st.markdown("Don't have an account? Sign up instead.")
        if st.button(REGISTER_BUTTON):
            st.session_state.screen = REGISTER_SCREEN
            st.rerun()

    def register_screen(self, callback: Callable):
        st.title("Create an account")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button(REGISTER_BUTTON):
            if st.session_state.screen == REGISTER_SCREEN:
                st.session_state.logged_in, name = self._register(name=name, username=username, password=password)
                if st.session_state.logged_in:
                    st.session_state.user = username
                    st.session_state.name = name if name != "" else username
                    callback()
                    st.rerun()

        st.markdown("Already have an account? Sign in instead.")
        if st.button(LOGIN_BUTTON):
            st.session_state.screen = LOGIN_SCREEN
            st.rerun()

    @staticmethod
    def entry_screen():
        # This contains buttons for selecting to login or sign up.
        st.title("Welcome! Please log in or sign up to continue.")
        if st.button(LOGIN_BUTTON):
            st.session_state.screen = LOGIN_SCREEN
            st.rerun()

        if st.button(REGISTER_BUTTON):
            st.session_state.screen = REGISTER_SCREEN
            st.rerun()