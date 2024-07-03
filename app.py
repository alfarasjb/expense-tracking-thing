import logging


import streamlit as st


from src.app.app import ExpenseTrackerApp

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ExpenseTrackerApp().main()


