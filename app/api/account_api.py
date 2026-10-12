from fastapi import APIRouter, Depends, Query

from app.database.database import get_session
from app.dtos.filters.account_search import AccountSearch
from app.services import account_service


router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/")
def accounts(
    search:AccountSearch = Depends(), 
    page:int = Query(ge=1, default=1), 
    size:int = Query(ge=10, default=10), 
    session=Depends(get_session)):

    return account_service.search(search, page, size, session)