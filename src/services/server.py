import json
import logging
from typing import Dict, Any, List, Optional, Tuple

import requests

from src.definitions.urls import Urls
from src.utils.decorators import on_http_error

"""
Communicates with node server
"""

logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        self.urls = Urls()

    @staticmethod
    def _get_key_from_json_response(response: requests.Response, key: str) -> Any:
        return json.loads(response.content).get(key)

    @on_http_error
    def store_data_to_db(self, payload: Dict[str, Any]) -> int:
        endpoint = self.urls.store_data_endpoint()
        logger.info(f"Storing expense data. Endpoint: {endpoint}, Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        return response.status_code

    @on_http_error
    def get_monthly_data(self, start_date, end_date) -> Tuple[List[Dict[str, Any]], str]:

        payload = dict(start_date=start_date, end_date=end_date)
        endpoint = self.urls.monthly_data_endpoint()
        logger.info(f"Getting expense data from {start_date} to {end_date}. Endpoint: {endpoint}. Payload: {payload}")
        response = requests.get(endpoint, json=payload)
        return self._get_key_from_json_response(response, key='data'), self._get_key_from_json_response(response, key='summary')

    @on_http_error
    def get_historical_data(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        endpoint = self.urls.expense_history_endpoint()
        response = requests.get(endpoint, json=payload)
        logger.info(f"Getting expense data. Endpoint: {endpoint}. Payload: {payload}")
        return self._get_key_from_json_response(response, key='data')

    @on_http_error
    def clear_database_contents(self) -> int:
        endpoint = self.urls.clear_database_contents_endpoint()
        response = requests.post(endpoint)
        return response.status_code

    @on_http_error
    def register_user(self, username: str, password: str) -> bool:
        payload = dict(username=username, password=password)
        endpoint = self.urls.register_endpoint()
        logger.info(f"Requesting to register user. Endpoint: {endpoint}. Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        success = response.status_code == 200
        if not success:
            logger.error(f"Failed to register user: {username}. Status Code: {response.status_code}")
        return success

    @on_http_error
    def login_user(self, username: str, password: str) -> bool:
        payload = dict(username=username, password=password)
        endpoint = self.urls.login_endpoint()
        logger.info(f"Requesting to authenticate user. Endpoint: {endpoint}. Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        success = response.status_code == 200
        if not success:
            logger.error(f"Failed to login user: {username}. Status Code: {response.status_code}. Endpoint: {endpoint}")
        return success

    @on_http_error
    def send_message_to_chatbot(self, user: str, message: str) -> Optional[str]:
        payload = dict(user=user, message=message)
        endpoint = self.urls.chatbot_message_endpoint()
        logger.info(f"Sending message to chatbot. Endpoint: {endpoint}. Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        if response.status_code == 200:
            message = self._get_key_from_json_response(response, key='message')
            return message
