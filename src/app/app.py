import logging
import datetime
from datetime import datetime as dt, timedelta

import pandas as pd
import streamlit as st
from src.app.plots import Plots
from src.definitions.enums import ExpenseCategory
from src.definitions.messages import Messages
from src.services.server import Server
from src.utils.decorators import authentication
from src.utils.utils import response_as_dataframe

logger = logging.getLogger(__name__)


# TODO: Dashboard
# TODO: Callback: Update dashboard on new entries (Fix this)

class ExpenseTrackerApp:
    def __init__(self):
        self.server = Server()
        self.plots = Plots()
        self._initialize_app()

    @property
    def _expense_categories(self):
        return [category.value for category in ExpenseCategory]

    @staticmethod
    def _initialize_app():
        st.set_page_config(page_title="Expense Tracker", layout="centered", initial_sidebar_state='collapsed')

    @staticmethod
    def _validate_float_input(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    @authentication(success_msg=Messages.login_success_message(), fail_msg=Messages.login_failed_message())
    def _login(self, username: str, password: str) -> bool:
        return self.server.login_user(username=username, password=password)

    @authentication(success_msg=Messages.register_success_message(), fail_msg=Messages.register_failed_message())
    def _register(self, username: str, password: str) -> bool:
        logger.info(f"Registering user with username: {username}, password: {password}")
        return self.server.register_user(username=username, password=password)

    @staticmethod
    def _valid_home_page_inputs(valid_option: bool, valid_fields: bool, valid_float_input: bool) -> bool:
        if not valid_option:
            st.error("Please select a category")
            return False
        if not valid_fields:
            st.error("Please complete all fields.")
            return False
        if not valid_float_input:
            st.error("Invalid amount. Numeric values only.")
            return False
        return True

    def _on_press_store_button(self, selected_option: str, expense_description: str, amount: str, selected_date: datetime.date):
        # Validation
        valid_option = selected_option != ExpenseCategory.DEFAULT.value
        valid_fields = (expense_description != "") or (amount != "")
        valid_float_input = self._validate_float_input(amount)

        if st.button("Store", use_container_width=True):
            valid_homepage_inputs = self._valid_home_page_inputs(
                valid_option=valid_option,
                valid_fields=valid_fields,
                valid_float_input=valid_float_input)
            try:
                if valid_homepage_inputs:
                    date = (datetime.datetime.combine(selected_date, datetime.time.min) + timedelta(days=1)).timestamp() * 1000  # Converts to datetime then gets timestamp
                    payload = {
                        "username": st.session_state.user,
                        "category": selected_option,
                        "description": expense_description,
                        "amount": amount,
                        "date": date
                    }
                    code = self.server.store_data_to_db(payload=payload)
                    st.session_state.refresh_dashboard = True
                    st.session_state.screen = "home"
                    if code == 200:
                        st.success("Expenses stored to database.")
                        self._on_refresh_monthly_data()
                        st.rerun()
                    else:
                        st.error("Something went wrong. Failed to log expenses into database.")
            except:
                pass

    def _on_press_expense_history_button(self):
        if st.button("Show Expense History", use_container_width=True):
            payload = {
                "username": st.session_state.user
            }
            data = self.server.get_historical_data(payload)
            st.dataframe(response_as_dataframe(data))

    def _chat_box(self):
        messages = st.container(height=500)

        # Initialize Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = [dict(role="assistant", content=f"Hello {st.session_state.user}! How can I help you today?")]

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            messages.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input("Say something"):
            messages.chat_message("user").write(prompt)
            user_message = dict(role="user", content=prompt)
            st.session_state.messages.append(user_message)
            bot_response = self.server.send_message_to_chatbot(user=st.session_state.user, message=prompt)
            if bot_response:
                messages.chat_message("assistant").write(bot_response)
                bot_message = dict(role="assistant", content=bot_response)
                st.session_state.messages.append(bot_message)

    def _on_press_clear_database_button(self):
        if st.button("Clear database contents", use_container_width=True):
            self.server.clear_database_contents()

    def add_expenses(self):
        selected_option = self._get_expense_category()
        expense_description = st.text_input("DESCRIPTION")
        amount = st.text_input("AMOUNT (Php)")
        selected_date = st.date_input(
            "Select a date",
            value=datetime.date.today(),
            min_value=datetime.date(2000, 1, 1),
            max_value=datetime.date.today())
        self._on_press_store_button(
            selected_option=selected_option,
            expense_description=expense_description,
            amount=amount,
            selected_date=selected_date
        )
        self._on_press_exit_button()

    def _on_press_exit_button(self):
        if st.button("Exit", use_container_width=True):
            # TODO: Update monthly data before rerun
            self._on_refresh_monthly_data()
            st.session_state.screen = "home"
            st.rerun()

    def _home_screen(self, on_callback=False):
        st.title(f"Welcome, {st.session_state.user}!")
        if st.button("Add Expenses"):
            st.session_state.screen = "expense_form"
            st.rerun()
        with st.sidebar:
            self._chat_box()
        self._dashboard()

    def _dashboard(self):
        if "summary" in st.session_state:
            st.write(st.session_state.summary)
        if "plot" in st.session_state:
            st.pyplot(st.session_state.plot)
        if "monthly_data" in st.session_state:
            st.dataframe(st.session_state.monthly_data, hide_index=True, use_container_width=True)
        else:
            print("Dashboard is up to date")

    def _get_monthly_data(self):
        date_fmt = "%m-%d-%Y"
        start_date = dt(dt.now().year, dt.now().month, 1)
        next_month = 1 if start_date.month == 12 else start_date.month + 1
        end_date = dt(start_date.year, next_month, 1)
        monthly_data, summary = self.server.get_monthly_data(start_date.strftime(date_fmt), end_date.strftime(date_fmt))
        st.session_state.monthly_data = monthly_data
        df = response_as_dataframe(monthly_data)
        return df, start_date, end_date, summary

        # st.dataframe(df, hide_index=True)

    def _get_expense_category(self) -> str:
        options = self._expense_categories
        selected_option = st.selectbox("CATEGORY", options)
        return selected_option
    
    def login_screen(self):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if st.session_state.screen == 'login':
                st.session_state.logged_in = self._login(username=username, password=password)
                if st.session_state.logged_in:
                    st.session_state.user = username
                    self._on_refresh_monthly_data()
                    st.rerun()
                st.error("Failed to login. Username or password may be incorrect.")

        # if st.button("Register"):
        #     st.session_state.screen = 'register'
        #     st.rerun()

    def _on_refresh_monthly_data(self):
        st.session_state.refresh_monthly_data = False
        st.session_state.monthly_data, start_date, end_date, summary = self._get_monthly_data()
        st.session_state.plot = self.plots.plot_monthly_expenses_bar_chart(st.session_state.monthly_data,
                                                                           start_date=start_date,
                                                                           end_date=end_date)
        if st.session_state.summary == "":
            st.session_state.summary = summary

    def register_screen(self):
        st.title("Create an account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.session_state.screen = "login"
            st.rerun()

        if st.button("Register"):
            if st.session_state.screen == 'register':
                st.session_state.logged_in = self._register(username=username, password=password)
                if st.session_state.logged_in:
                    st.rerun()
                st.error("Failed to register.")

    def _initialize_session_state(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "screen" not in st.session_state:
            st.session_state.screen = "login"
        if "refresh_dashboard" not in st.session_state:
            st.session_state.refresh_dashboard = True
        if "user" not in st.session_state:
            st.session_state.user = ""
        if "summary" not in st.session_state:
            st.session_state.summary = ""

    def main(self):
        self._initialize_session_state()

        print("SCREEN: ", st.session_state.screen)
        if not st.session_state.logged_in:
            if st.session_state.screen == 'login':
                self.login_screen()
            elif st.session_state.screen == 'register':
                self.register_screen()
        # if st.session_state.screen == "expense_form":
        #     self.add_expenses()
        else:
            if st.session_state.screen == "expense_form":
                self.add_expenses()
            else:
                self._home_screen()
