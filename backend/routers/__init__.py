from fastapi import APIRouter

from .users import router as users_router
from .habits import router as habits_router

router = APIRouter()
router.include_router(users_router)
router.include_router(habits_router)
