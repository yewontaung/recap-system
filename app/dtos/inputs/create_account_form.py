from app.dtos.base import BaseDto


class CreateAccountForm(BaseDto):
    username: str
    fullname: str
    reference_id: str | None = None
