from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=100)
    password: SecretStr = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str