from loader import dp

from . import actions, base, help, info, start  # noqa: F401
from .routers import admins_router

dp.include_router(admins_router)
