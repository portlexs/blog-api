import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.token_model import Token
from ..schemas.token_schemas import TokenPayload


class TokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_token(self, jti: uuid.UUID) -> Optional[Token]:
        query = select(Token).where(Token.jti == jti)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def save_token(self, token_payload: TokenPayload) -> Token:
        token = Token(
            jti=token_payload.jti,
            user_id=token_payload.user_data.id,
            created_at=token_payload.iat,
            expires_at=token_payload.exp,
            is_revoked=False,
        )

        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)

        return token

    async def revoke_token(self, token: Token) -> Token:
        token.is_revoked = True
        await self.session.commit()
        await self.session.refresh(token)

        return token
