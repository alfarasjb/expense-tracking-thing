import requests
from typing import Dict, Any
from src.definitions.urls import Urls
"""
Communicates with node server
"""


class Server:
    def __init__(self):
        self.urls = Urls()

    def store_data_to_db(self, payload: Dict[str, Any]):
        endpoint = self.urls.store_data_endpoint()
        response = requests.post(endpoint, json=payload)
        return response

    def get_monthly_data(self, start_date, end_date):
        payload = {
            "start_date": start_date,
            "end_date": end_date
        }
        endpoint = self.urls.monthly_data_endpoint()
        response = requests.get(endpoint, json=payload)
        return response

    def get_historical_data(self):
        endpoint = self.urls.expense_history_endpoint()
        response = requests.get(endpoint)
        return response
