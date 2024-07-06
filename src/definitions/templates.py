from dataclasses import dataclass


@dataclass
class UserTemplate:
    name: str
    username: str
    password: str
