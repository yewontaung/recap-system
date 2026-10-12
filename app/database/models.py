from enum import Enum
from typing import Optional
from uuid import UUID
import uuid

from sqlmodel import Field, Relationship

from app.database.base import AuditableModel


class Account(AuditableModel, table=True):

    account_id:Optional[int] = Field(primary_key=True, default=None)
    username:str = Field(index=True, nullable=False, unique=True)
    email:str = Field(index=True, nullable=True, unique=True)
    fullname:str = Field(nullable=False)

    class Role(str, Enum):
        USER = "user"
        ADMIN = "admin"

    class SignUpPolicy(str, Enum):
        MANUAL = "manual"
        GOOGLE = "google"
        TELEGRAM = "telegram"

    role:Role = Field(default=Role.USER)
    sign_up_policy:SignUpPolicy = Field(default=SignUpPolicy.MANUAL)
    reference_id:Optional[str] = Field(default=None, nullable=True)

    profile_url:Optional[str] = Field(default=None, nullable=True)

    api_keys:list["AIApiKey"] = Relationship(back_populates="account")

class AccountPassword(AuditableModel, table=True):
    account_id:Optional[int] = Field(primary_key=True, foreign_key="account.account_id")
    hashed_password:str = Field(nullable=False)
    account:Account = Relationship()

class AIApiKey(AuditableModel, table=True):
    key_id:Optional[UUID] = Field(primary_key=True, default_factory=uuid.uuid4)
    hashed_key:str = Field(nullable=False)

    account_id:int = Field(nullable=False, foreign_key="account.account_id")
    account:Account = Relationship(back_populates="api_keys")
    