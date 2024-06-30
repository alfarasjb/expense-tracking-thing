from datetime import datetime as dt
from functools import wraps

import streamlit as st

from src.definitions.enums import ExpenseCategory
from src.services.server import Server

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  # Log to a file
                        logging.StreamHandler()  # Also log to console
                    ])

# Create a logger
logger = logging.getLogger(__name__)


def authentication(success_msg: str, fail_msg: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            try:
                response = func(*args, **kwargs)
                success = response.status_code == 200
                if success:
                    st.success(success_msg)
                else:
                    st.error(fail_msg)
                return success
            except Exception:
                print("An unknown error occurred")
                return False
        return wrapper
    return decorator


class ExpenseTrackerApp:
    def __init__(self):
        self.server = Server()
        self._initialize_app()

    @property
    def _expense_categories(self):
        return [category.value for category in ExpenseCategory]

    @staticmethod
    def _initialize_app():
        st.set_page_config(page_title="Expense Tracker", layout="centered")

    @staticmethod
    def _validate_float_input(value: str):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @authentication(
        success_msg="Logged in successfully",
        fail_msg="Failed to login. Username or password may be incorrect")
    def _login(self, username: str, password: str) -> bool:
        return self.server.login_user(username=username, password=password)

    @authentication(
        success_msg="User registered successfully",
        fail_msg="Failed to register. Username may already exist")
    def _register(self, username: str, password: str) -> bool:
        logger.info(f"Registering user with username: {username}, password: {password}")
        return self.server.register_user(username=username, password=password)

    @staticmethod
    def _valid_home_page_inputs(valid_option: bool, valid_fields: bool, valid_float_input: bool):
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

    def _on_press_store_button(self, selected_option: str, expense_description: str, amount: str):
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
                    payload = {
                        "category": selected_option,
                        "description": expense_description,
                        "amount": amount
                    }
                    response = self.server.store_data_to_db(payload=payload)
                    if response.status_code == 200:
                        st.success("Expenses stored to database.")
                    else:
                        st.error("Something went wrong. Failed to log expenses into database.")
            except:
                pass

    def _on_press_expense_history_button(self):
        if st.button("Show Expense History", use_container_width=True):
            self.server.get_historical_data()

    def _on_press_monthly_expense_button(self):
        if st.button("Generate Monthly Expense Report", use_container_width=True):
            date_fmt = "%m-%d-%Y"
            start_date = dt(dt.now().year, dt.now().month, 1).strftime(date_fmt)
            end_date = dt.now().strftime(date_fmt)
            monthly_data = self.server.get_monthly_data(start_date, end_date)

    def _on_press_clear_database_button(self):
        if st.button("Clear database contents", use_container_width=True):
            self.server.clear_database_contents()

    def _home_screen(self):
        st.title("Expense Tracker")
        selected_option = self._get_expense_category()
        expense_description = st.text_input("Description")
        amount = st.text_input("Amount (Php)")
        self._on_press_store_button(
            selected_option=selected_option,
            expense_description=expense_description,
            amount=amount
        )
        self._on_press_expense_history_button()
        self._on_press_monthly_expense_button()
        self._on_press_clear_database_button()

    def _get_expense_category(self):
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
                    st.rerun()
                st.error("Failed to login. Username or password may be incorrect.")

        if st.button("Register"):
            st.session_state.screen = 'register'
            st.rerun()

    def register_screen(self):
        st.title("Create an account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.session_state.screen = "login"
            st.rerun()

        if st.button("Register"):
            print("register")
            if st.session_state.screen == 'register':
                print(f"Registering: {username}, {password}")
                st.session_state.logged_in = self._register(username=username, password=password)
                if st.session_state.logged_in:
                    st.rerun()
                st.error("Failed to register.")

    def main(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "screen" not in st.session_state:
            st.session_state.screen = "login"

        if not st.session_state.logged_in:
            if st.session_state.screen == 'login':
                self.login_screen()
            elif st.session_state.screen == 'register':
                self.register_screen()
        else:
            self._home_screen()
