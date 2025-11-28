from datetime import timedelta
from enum import Enum


class TokenType(Enum):
    ACCESS = timedelta(minutes=60)
    REFRESH = timedelta(days=30)
