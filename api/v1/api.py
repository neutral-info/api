from fastapi import APIRouter
from api.v1.endpoints import keyword, item


prefix = "/api/v1"
api_router = APIRouter()
api_router.include_router(keyword.router, prefix=prefix)
api_router.include_router(item.router, prefix=prefix)
