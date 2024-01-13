from loader import dp

from . import errors  # noqa: F401
from .routers import errors_router

dp.include_router(errors_router)
