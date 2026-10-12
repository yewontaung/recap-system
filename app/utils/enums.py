from enum import Enum


class ClientType(str, Enum):
    WEB = "web"
    TELEGRAM = "telegram"