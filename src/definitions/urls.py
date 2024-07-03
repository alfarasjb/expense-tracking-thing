

class Urls:
    def __init__(self):
        self.server_host = 'expense-tracker-server.fly.dev'
        self.server_port = 3000
        self.base_url = f'http://{self.server_host}'
        self.db_url = f'{self.base_url}/api/db'

    def monthly_data_endpoint(self) -> str:
        return f'{self.db_url}/monthly-data'

    def store_data_endpoint(self) -> str:
        return f'{self.db_url}/store'

    def expense_history_endpoint(self) -> str:
        return f'{self.db_url}/history'

    def clear_database_contents_endpoint(self) -> str:
        return f'{self.db_url}/clear-db'

    def register_endpoint(self) -> str:
        return f'{self.db_url}/auth-register'

    def login_endpoint(self) -> str:
        return f'{self.db_url}/auth-login'
