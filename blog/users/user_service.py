from users.user_schemas import PublicUser, UserCreate


class UserService:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_in: UserCreate) -> PublicUser:
        raise NotImplementedError()
