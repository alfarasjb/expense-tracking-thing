

class Urls:
    def __init__(self):
        self.server_host = None
        self.server_port = None
        self.base_url = f'http://{self.server_host}:{self.server_port}'

    def monthly_data_endpoint(self) -> str:
        return f'{self.base_url}/api/db/monthly-data'
    