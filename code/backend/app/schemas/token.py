from typing import Optional

from pydantic import BaseModel

from app.schemas.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User
