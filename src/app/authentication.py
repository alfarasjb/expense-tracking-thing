from typing import Callable

import streamlit as st

from src.definitions.constants import LOGIN_BUTTON, LOGIN_SCREEN, REGISTER_BUTTON, REGISTER_SCREEN
from src.definitions.messages import Messages
from src.services.server import server
from src.utils.decorators import authentication


class Authentication:
    def __init__(self):
        self.server = server

    @authentication(success_msg=Messages.login_success_message(), fail_msg=Messages.login_failed_message())
    def _login(self, username: str, password: str) -> bool:
        return self.server.login_user(username=username, password=password)

    @authentication(success_msg=Messages.register_success_message(), fail_msg=Messages.register_failed_message())
    def _register(self, username: str, password: str) -> bool:
        return self.server.register_user(username=username, password=password)

    """ 
    Screens
    """
    def login_screen(self, callback: Callable):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button(LOGIN_BUTTON):
            if st.session_state.screen == LOGIN_SCREEN:
                st.session_state.logged_in = self._login(username=username, password=password)
                if st.session_state.logged_in:
                    st.session_state.user = username
                    callback()
                    st.rerun()
                st.error("Failed to login. Username or password may be incorrect.")

    def register_screen(self):
        st.title("Create an account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button(LOGIN_BUTTON):
            st.session_state.screen = LOGIN_SCREEN
            st.rerun()

        if st.button(REGISTER_BUTTON):
            if st.session_state.screen == REGISTER_SCREEN:
                st.session_state.logged_in = self._register(username=username, password=password)
                if st.session_state.logged_in:
                    st.rerun()
                st.error("Failed to register")