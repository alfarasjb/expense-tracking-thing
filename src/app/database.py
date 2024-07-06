import datetime
import logging
from datetime import timedelta, datetime as dt
from typing import List, Dict, Union, Any

import pandas as pd
import streamlit as st

from src.app.plots import Plots
from src.definitions.constants import (
    STORE_BUTTON,
    HOME_SCREEN,
    EXIT_BUTTON,
    SHOW_EXPENSE_HISTORY_BUTTON,
    CLEAR_DATABASE_CONTENTS)
from src.definitions.enums import ExpenseCategory
from src.services.server import server
from src.utils.utils import validate_float_input, response_as_dataframe
from src.app.events import set_screen

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.server = server
        self.plots = Plots()

    """
    Screen
    """
    def add_expenses_screen(self):
        selected_option = self._get_expense_category()
        expense_description = st.text_input("DESCRIPTION")
        amount = st.text_input("AMOUNT (Php)")
        selected_date = st.date_input(
            "Select a date",
            value=datetime.date.today(),
            min_value=datetime.date(2000, 1, 1),
            max_value=datetime.date.today())
        store_bt, exit_bt = st.columns(2)
        store_bt.button(STORE_BUTTON, use_container_width=True, on_click=self._on_press_store_button, args=[selected_option, expense_description, amount, selected_date])
        exit_bt.button(EXIT_BUTTON, use_container_width=True, on_click=self._on_press_exit_button)

    """ 
    Events
    """
    def _on_press_exit_button(self):
        set_screen(HOME_SCREEN)
        self.on_refresh_monthly_data()

    def _on_press_expense_history_button(self):
        if st.button(SHOW_EXPENSE_HISTORY_BUTTON, use_container_width=True):
            payload = {
                "username": st.session_state.user
            }
            data = self.server.get_historical_data(payload)
            st.dataframe(response_as_dataframe(data))

    def _on_press_clear_database_button(self):
        if st.button(CLEAR_DATABASE_CONTENTS, use_container_width=True):
            self.server.clear_database_contents()

    def _on_press_store_button(self, selected_option: str, expense_description: str, amount: str,
                               selected_date: datetime.date):
        # Validation
        valid_option = selected_option != ExpenseCategory.DEFAULT.value
        valid_fields = (expense_description != "") or (amount != "")
        valid_float_input = validate_float_input(amount)

        valid_homepage_inputs = self._valid_home_page_inputs(
            valid_option=valid_option,
            valid_fields=valid_fields,
            valid_float_input=valid_float_input)
        try:
            if valid_homepage_inputs:
                date = (datetime.datetime.combine(selected_date, datetime.time.min) + timedelta(
                    days=1)).timestamp() * 1000  # Converts to datetime then gets timestamp
                payload = {
                    "username": st.session_state.user,
                    "category": selected_option,
                    "description": expense_description,
                    "amount": amount,
                    "date": date
                }
                code = self.server.store_data_to_db(payload=payload)
                st.session_state.refresh_dashboard = True
                if code == 200:
                    st.success("Expenses stored to database.")
                    self.on_refresh_monthly_data()
                else:
                    st.error("Something went wrong. Failed to log expenses into database.")
        except:
            pass

    def on_refresh_monthly_data(self):
        # TODO: Add validation if there's no data
        st.session_state.refresh_monthly_data = False
        st.session_state.monthly_data, start_date, end_date, summary = self._get_monthly_data()
        if st.session_state.monthly_data is not None:
            st.session_state.plot = self.plots.plot_monthly_expenses_bar_chart(
                st.session_state.monthly_data,
                start_date=start_date,
                end_date=end_date)
        st.session_state.summary = summary

    """
    Helpers
    """
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

    @property
    def _expense_categories(self):
        return [category.value for category in ExpenseCategory]

    def _get_expense_category(self) -> str:
        options = self._expense_categories
        selected_option = st.selectbox("CATEGORY", options)
        return selected_option

    def _get_monthly_data(self):
        date_fmt = "%m-%d-%Y"
        start_date = dt(dt.now().year, dt.now().month, 1)
        next_month = 1 if start_date.month == 12 else start_date.month + 1
        end_date = dt(start_date.year, next_month, 1)
        monthly_data, summary = self.server.get_monthly_data(start_date.strftime(date_fmt), end_date.strftime(date_fmt))
        data_is_available = self._check_for_available_data(monthly_data, summary)
        if not data_is_available:
            logger.info(f"No data available for {start_date} to {end_date}")
            return None, start_date, end_date, None
        df = response_as_dataframe(monthly_data)
        return df, start_date, end_date, summary

    @staticmethod
    def _check_for_available_data(monthly_data: Union[List[Dict[str, Any]], str], summary: str):
        if isinstance(monthly_data, str):
            return False
        if summary == "":
            return False
        return True
