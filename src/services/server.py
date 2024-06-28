import requests

"""
Communicates with node server
"""


class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5000

    def test_endpoint_request(self):
        endpoint = f'http://{self.host}:{self.port}/test'
        response = requests.get(endpoint)
        return response

    def test_post_request_with_payload(self, payload):
        endpoint = f'http://{self.host}:{self.port}/test'
        response = requests.post(endpoint, json=payload)
        return response

    def get_monthly_data(self, start_date, end_date):
        payload = {
            "start_date": start_date,
            "end_date": end_date
        }

