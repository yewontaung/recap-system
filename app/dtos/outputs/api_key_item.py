from app.dtos.base import BaseDto


class APIKeyItem(BaseDto):
    key_id: str
    hashed_key: str
    account_id: int
    username: str
    fullname: str
    profile_url: str