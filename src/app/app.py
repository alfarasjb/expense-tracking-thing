import logging

import streamlit as st

from src.app.authentication import Authentication
from src.app.chat import Chat
from src.app.database import Database
from src.definitions import constants as c
from src.services.server import server

logger = logging.getLogger(__name__)


class ExpenseTrackerApp:
    def __init__(self):
        self.server = server
        self.chat = Chat()
        self.authentication = Authentication()
        self.db = Database()
        self._initialize_app()

    @staticmethod
    def _initialize_app():
        st.set_page_config(page_title="Expense Tracker", layout="centered", initial_sidebar_state='collapsed')

    def _home_screen(self):
        st.title(f"Welcome, {st.session_state.user}!")
        if st.button(c.ADD_EXPENSES_BUTTON):
            st.session_state.screen = c.EXPENSE_SCREEN
            st.rerun()
        with st.sidebar:
            self.chat.chat_box()
        self._dashboard()

    @staticmethod
    def _dashboard():
        if "summary" in st.session_state:
            st.write(st.session_state.summary)
        if "plot" in st.session_state:
            st.pyplot(st.session_state.plot)
        if "monthly_data" in st.session_state:
            st.dataframe(st.session_state.monthly_data, hide_index=True, use_container_width=True)
        else:
            print("Dashboard is up to date")

    @staticmethod
    def _initialize_session_state():
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "screen" not in st.session_state:
            st.session_state.screen = c.LOGIN_SCREEN
        if "refresh_dashboard" not in st.session_state:
            st.session_state.refresh_dashboard = True
        if "user" not in st.session_state:
            st.session_state.user = ""
        if "summary" not in st.session_state:
            st.session_state.summary = ""

    def main(self):
        self._initialize_session_state()
        if not st.session_state.logged_in:
            if st.session_state.screen == c.LOGIN_SCREEN:
                self.authentication.login_screen(self.db.on_refresh_monthly_data)
            elif st.session_state.screen == c.REGISTER_SCREEN:
                self.authentication.register_screen()
        else:
            if st.session_state.screen == c.EXPENSE_SCREEN:
                self.db.add_expenses_screen()
            else:
                self._home_screen()
