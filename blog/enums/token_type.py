from datetime import timedelta
from enum import Enum


class TokenType(Enum):
    ACCESS = timedelta(minutes=30)
    REFRESH = timedelta(days=30)
