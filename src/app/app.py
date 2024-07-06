import logging

import streamlit as st

from src.app.authentication import Authentication
from src.app.chat import Chat
from src.app.database import Database
from src.definitions import constants as c
from src.services.server import server
from src.app.events import set_screen

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

    @staticmethod
    def _on_click_sign_out_button():
        set_screen(c.ENTRY_SCREEN)
        st.session_state.user = ""
        st.session_state.summary = ""
        st.session_state.name = ""
        st.session_state.logged_in = False

    def _home_screen(self):
        st.header(f"Welcome, {st.session_state.name}!")
        profile, sign_out, _ = st.columns([1, 1, 3])
        profile.button("View Profile", use_container_width=True)
        sign_out.button("Sign out", use_container_width=True, on_click=self._on_click_sign_out_button)
        # st.button(c.ADD_EXPENSES_BUTTON, on_click=set_screen, args=[c.EXPENSE_SCREEN])
        with st.sidebar:
            self.chat.chat_box()
        self._dashboard()

    @staticmethod
    def _get_summary():
        if "summary" in st.session_state and st.session_state.summary:
            return st.session_state.summary
        return "No data available for the currrent month."

    def _dashboard(self):
        st.write(self._get_summary())
        if "plot" in st.session_state:
            st.pyplot(st.session_state.plot)
        st.header("Expenses")
        add_expenses, view_all_expenses, _ = st.columns([2, 2, 4])
        add_expenses.button(c.ADD_EXPENSES_BUTTON, use_container_width=True, on_click=set_screen, args=[c.EXPENSE_SCREEN])
        view_all_expenses.button("View All Expenses", use_container_width=True, on_click=set_screen, args=[c.HISTORY_SCREEN])

        if "monthly_data" in st.session_state and st.session_state.monthly_data is not None:
            st.dataframe(st.session_state.monthly_data, hide_index=True, use_container_width=True)
        else:
            logger.info("Dashboard is up to date.")

    @staticmethod
    def _initialize_session_state():
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "screen" not in st.session_state:
            set_screen(c.ENTRY_SCREEN)
        if "refresh_dashboard" not in st.session_state:
            st.session_state.refresh_dashboard = True
        if "user" not in st.session_state:
            st.session_state.user = ""
        if "summary" not in st.session_state:
            st.session_state.summary = ""
        if "name" not in st.session_state:
            st.session_state.name = ""

    def main(self):
        self._initialize_session_state()
        if not st.session_state.logged_in:
            if st.session_state.screen == c.ENTRY_SCREEN:
                self.authentication.entry_screen()
            elif st.session_state.screen == c.LOGIN_SCREEN:
                self.authentication.login_screen(self.db.on_refresh_monthly_data)
            elif st.session_state.screen == c.REGISTER_SCREEN:
                self.authentication.register_screen(self.db.on_refresh_monthly_data)
        else:
            if st.session_state.screen == c.EXPENSE_SCREEN:
                self.db.add_expenses_screen()
            elif st.session_state.screen == c.HISTORY_SCREEN:
                self.db.expenses_history_screen()
            else:
                self._home_screen()
