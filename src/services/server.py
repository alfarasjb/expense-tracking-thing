import logging
from typing import Dict, Any, List
import json
import requests

from src.definitions.urls import Urls

"""
Communicates with node server
"""

logger = logging.getLogger(__name__)


def on_http_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.ConnectionError:
            err_msg = "Request failed. Connection is not found"
            logger.error(err_msg)
            raise requests.exceptions.ConnectionError(err_msg)
        except Exception:
            logger.error("Request failed. An unknown error occurred.")
    return wrapper


class Server:
    def __init__(self):
        self.urls = Urls()

    @on_http_error
    def store_data_to_db(self, payload: Dict[str, Any]) -> int:
        endpoint = self.urls.store_data_endpoint()
        response = requests.post(endpoint, json=payload)
        return response.status_code

    @on_http_error
    def get_monthly_data(self, start_date, end_date) -> List[Dict[str, Any]]:
        payload = dict(start_date=start_date, end_date=end_date)
        endpoint = self.urls.monthly_data_endpoint()
        response = requests.get(endpoint, json=payload)
        return json.loads(response.content.get('data'))

    @on_http_error
    def get_historical_data(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        endpoint = self.urls.expense_history_endpoint()
        response = requests.get(endpoint, json=payload)
        return json.loads(response.content.get('data'))

    @on_http_error
    def clear_database_contents(self) -> int:
        endpoint = self.urls.clear_database_contents_endpoint()
        response = requests.post(endpoint)
        return response.status_code

    @on_http_error
    def register_user(self, username: str, password: str) -> bool:
        payload = dict(username=username, password=password)
        endpoint = self.urls.register_endpoint()
        response = requests.post(endpoint, json=payload)
        return response.status_code == 200

    @on_http_error
    def login_user(self, username: str, password: str) -> bool:
        payload = dict(username=username, password=password)
        endpoint = self.urls.login_endpoint()
        response = requests.post(endpoint, json=payload)
        return response.status_code == 200
