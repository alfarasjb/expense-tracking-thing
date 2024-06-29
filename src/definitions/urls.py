

class Urls:
    def __init__(self):
        self.server_host = 'localhost'
        self.server_port = 5000
        self.base_url = f'http://{self.server_host}:{self.server_port}'
        self.db_url = f'{self.base_url}/api/db'

    def monthly_data_endpoint(self) -> str:
        return f'{self.db_url}/monthly-data'

    def store_data_endpoint(self) -> str:
        return f'{self.db_url}/store'

    def expense_history_endpoint(self) -> str:
        return f'{self.db_url}/history'
