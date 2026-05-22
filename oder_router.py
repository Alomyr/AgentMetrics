from fastapi import APIRouter

oder_routers = APIRouter(prefix="/oder", tags=["oder"])


@oder_routers.get("/")