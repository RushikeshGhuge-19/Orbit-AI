from uuid import uuid4

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user_data: UserCreate) -> User:

        existing_email = await self.repository.get_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already registered")

        existing_username = await self.repository.get_by_username(
            user_data.username
        )
        if existing_username:
            raise ValueError("Username already taken")

        user = User(
            id=uuid4(),
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(
                user_data.password.get_secret_value()
            ),
        )

        return await self.repository.create(user)

    async def login(self, email: str, password: str) -> Token:

        user = await self.repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Inactive account")

        token = create_access_token(subject=str(user.id))

        return Token(
            access_token=token,
            token_type="bearer",
        )