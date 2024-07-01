

class Messages:

    @classmethod
    def login_success_message(cls) -> str:
        return "Logged in successfully."

    @classmethod
    def login_failed_message(cls) -> str:
        return "Failed to login. Username or password may be incorrect."

    @classmethod
    def register_success_message(cls) -> str:
        return "User registered successfully."

    @classmethod
    def register_failed_message(cls) -> str:
        return "Failed to register. Username may already exist."
