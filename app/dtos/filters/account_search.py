from app.database.models import Account
from app.dtos.base import BaseDto


class AccountSearch(BaseDto):
    q: str | None = None
    sign_up_policy: Account.SignUpPolicy | None = None