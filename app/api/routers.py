from fastapi import APIRouter

from .endpoints import (
    charity_router, donation_router, gapi_router, user_router
)

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(gapi_router, prefix="/google", tags=["Google"])
main_router.include_router(charity_router, prefix="/charity_project", tags=[
    "Charity Projects"
])
main_router.include_router(donation_router, prefix="/donation", tags=[
    "Donations"
])
