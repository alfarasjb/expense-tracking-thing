from datetime import datetime as dt

import streamlit as st

from src.definitions.enums import ExpenseCategory
from src.services.server import Server


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

    def _validate_credentials(self):
        return True

    @staticmethod
    def _validate_float_input(value: str):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def login_screen(self):
        st.markdown("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if self._validate_credentials():
                st.session_state.logged_in = True
                st.rerun()  # Call this to create a new page
            else:
                st.error("Username or password maybe incorrect.")

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

    def _get_expense_category(self):
        options = self._expense_categories
        selected_option = st.selectbox("CATEGORY", options)
        return selected_option

    def main(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            self.login_screen()
        else:
            self._home_screen()
