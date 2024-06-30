import requests
from typing import Dict, Any
from src.definitions.urls import Urls
"""
Communicates with node server
"""


def on_http_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            print("Request failed. Connection is not found.")
        except Exception:
            print("Request failed. An unknown error occurred.")
    return wrapper


class Server:
    def __init__(self):
        self.urls = Urls()

    @on_http_error
    def store_data_to_db(self, payload: Dict[str, Any]):
        endpoint = self.urls.store_data_endpoint()
        response = requests.post(endpoint, json=payload)
        return response

    @on_http_error
    def get_monthly_data(self, start_date, end_date):
        payload = dict(start_date=start_date, end_date=end_date)
        endpoint = self.urls.monthly_data_endpoint()
        response = requests.get(endpoint, json=payload)
        return response

    @on_http_error
    def get_historical_data(self):
        endpoint = self.urls.expense_history_endpoint()
        response = requests.get(endpoint)
        return response

    @on_http_error
    def clear_database_contents(self):
        endpoint = self.urls.clear_database_contents_endpoint()
        response = requests.post(endpoint)
        print(response)
        return response

    @on_http_error
    def register_user(self, username: str, password: str):
        payload = dict(username=username, password=password)
        endpoint = self.urls.register_endpoint()
        response = requests.post(endpoint, json=payload)
        return response

    @on_http_error
    def login_user(self, username: str, password: str):
        payload = dict(username=username, password=password)
        endpoint = self.urls.login_endpoint()
        response = requests.post(endpoint, json=payload)
        return response
