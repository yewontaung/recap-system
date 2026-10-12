from sqlmodel import Session, func, select

from app.database.models import AIApiKey, Account
from app.dtos.base import UpdateResult
from app.dtos.inputs.api_key_form import APIKeyForm
from app.dtos.outputs.api_key_item import APIKeyItem
from app.utils.enums import ClientType


def add_api_key(form:APIKeyForm, client: ClientType, user_id:str, session:Session) -> UpdateResult:
    match client:
        case ClientType.TELEGRAM: return _add_api_key_via_telegram(form, user_id, session)

    raise ValueError(f"Unsupported client type: {client}")

def _add_api_key_via_telegram(form:APIKeyForm, user_id:str, session:Session) -> UpdateResult:
    account = session.exec(
        select(Account).where(Account.reference_id == user_id)
    ).first()

    if not account:
        raise ValueError(f"No account found for user_id {user_id}")

    api_key = AIApiKey(
        hashed_key=form.api_key,
        account_id=account.account_id
    )

    session.add(api_key)
    session.commit()
    session.refresh(api_key)

    return UpdateResult(resource_id=str(api_key.key_id))

def find_one_by_user_id(user_id:str, client:ClientType, session:Session) -> APIKeyItem:
    ...

def has_api_key_by_user_id(user_id:str, client:ClientType, session:Session) -> bool:

    if client == ClientType.TELEGRAM:
        account = session.exec(select(Account).where(Account.reference_id == user_id)).first()
    else:
        account = session.get(Account, user_id)

    total = session.exec(
        select(func.count(AIApiKey.key_id)).where(AIApiKey.account_id == account.account_id)
    ).one_or_none() or 0

    return total > 0