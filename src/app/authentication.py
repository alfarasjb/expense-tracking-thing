from typing import Callable, Tuple

import streamlit as st

from src.definitions.constants import LOGIN_BUTTON, LOGIN_SCREEN, REGISTER_BUTTON, REGISTER_SCREEN
from src.definitions.messages import Messages
from src.services.server import server
from src.utils.decorators import authentication
from src.definitions.templates import UserTemplate
from src.app.events import set_screen


class Authentication:
    def __init__(self):
        self.server = server

    """
    Server
    """
    @authentication(success_msg=Messages.login_success_message(), fail_msg=Messages.login_failed_message())
    def _login(self, user: UserTemplate) -> Tuple[bool, str]:
        # Put name here so we can use only 1 func
        username = user.username
        password = user.password
        return self.server.login_user(username=username, password=password)

    @authentication(success_msg=Messages.register_success_message(), fail_msg=Messages.register_failed_message())
    def _register(self, user: UserTemplate) -> Tuple[bool, str]:
        name = user.name
        username = user.username
        password = user.password
        return self.server.register_user(name=name, username=username, password=password)

    """ 
    Screens
    """
    def login_screen(self, callback: Callable):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        user = UserTemplate(name="", username=username, password=password)
        st.button(LOGIN_BUTTON, on_click=self._on_click_auth_button, args=[user, LOGIN_SCREEN, self._login, callback])
        st.markdown("Don't have an account? Sign up instead.")
        st.button(REGISTER_BUTTON, on_click=set_screen, args=[REGISTER_SCREEN])

    def register_screen(self, callback: Callable):
        st.title("Create an account")
        name = st.text_input("Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        user = UserTemplate(name, username, password)
        st.button(REGISTER_BUTTON, on_click=self._on_click_auth_button, args=[user, REGISTER_SCREEN, self._register, callback])
        st.markdown("Already have an account? Sign in instead.")
        st.button(LOGIN_BUTTON, on_click=set_screen, args=[LOGIN_SCREEN])

    def entry_screen(self):
        # This contains buttons for selecting to login or sign up.
        st.header("Welcome! Please log in or register to continue.")
        _, col_1, col_2, _ = st.columns([5, 2, 2, 5])
        col_1.button(LOGIN_BUTTON, on_click=self._on_click_button_from_entry, args=[LOGIN_SCREEN], use_container_width=True)
        col_2.button(REGISTER_BUTTON, on_click=self._on_click_button_from_entry, args=[REGISTER_SCREEN], use_container_width=True)

    """ 
    Events
    """
    @staticmethod
    def _on_click_button_from_entry(screen: str):
        st.session_state.screen = screen

    @staticmethod
    def _on_successful_login(name: str, username: str):
        st.session_state.user = username
        st.session_state.name = name if name != "" else username

    def _on_click_auth_button(self, user: UserTemplate, screen: str, func: Callable, callback: Callable):
        if st.session_state.screen == screen:
            st.session_state.logged_in, name = func(user)
            if st.session_state.logged_in:
                self._on_successful_login(name=name, username=user.username)
                callback()
