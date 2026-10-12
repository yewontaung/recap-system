from fastapi import APIRouter

from app.api import account_api


router = APIRouter()

router.include_router(router=account_api.router)