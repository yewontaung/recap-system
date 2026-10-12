from datetime import datetime

from app.database.models import Account
from app.dtos.base import BaseDto


class AccountItem(BaseDto):
    account_id: int
    username: str
    fullname: str
    profile_url: str | None = None
    reference_id: str | None = None
    sign_up_policy: Account.SignUpPolicy
    role: Account.Role
    created_at: datetime
    updated_at: datetime