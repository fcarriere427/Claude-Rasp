from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties to return via API
class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# Additional properties stored in DB
class UserInDB(User):
    hashed_password: str
