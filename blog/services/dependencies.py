from fastapi import Depends

from database.dependencies import get_db
from services.user_service import UserService


def get_user_service(db=Depends(get_db)) -> UserService:
    return UserService(db)
