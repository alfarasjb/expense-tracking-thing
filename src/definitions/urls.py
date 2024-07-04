from src.definitions.env_variables import EnvVariables

class Urls:
    def __init__(self):
        self.server_host = 'expense-tracker-server.fly.dev'
        self.server_port = 3000
        self.base_url = EnvVariables.server_base_url()
        self.db_url = f'{self.base_url}/api/db'
        self.chatbot_url = f'{self.base_url}/api/chat'

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

    def chatbot_message_endpoint(self) -> str:
        return f'{self.chatbot_url}/send-message'

