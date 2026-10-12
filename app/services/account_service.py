from sqlmodel import Session, select

from app.database.models import Account
from app.dtos.base import UpdateResult
from app.dtos.filters.account_search import AccountSearch
from app.dtos.inputs.create_account_form import CreateAccountForm
from app.dtos.outputs.account_item import AccountItem


def search(search:AccountSearch, page:int, size:int, session:Session) -> list[AccountItem]:
    return

def create_from_resource(form:CreateAccountForm, policy: Account.SignUpPolicy, session: Session) -> UpdateResult:

    match policy:
        case Account.SignUpPolicy.TELEGRAM: return _create_from_telegram(form, session)

    raise ValueError(f"Unsupported sign up policy: {policy}")
    
def _create_from_telegram(form:CreateAccountForm, session: Session) -> UpdateResult:

    query = select(Account).where(Account.reference_id == form.reference_id)
    if session.exec(query).first():
        raise ValueError(f"Account with reference_id {form.reference_id} already exists.")

    account = Account(
        username=form.username,
        fullname=form.fullname,
        reference_id=form.reference_id,
        sign_up_policy=Account.SignUpPolicy.TELEGRAM
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    
    return UpdateResult(resource_id=account.account_id)