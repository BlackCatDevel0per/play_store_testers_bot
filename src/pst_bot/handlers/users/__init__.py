from loader import dp  # noqa: I001

# TODO: Log enabled modules/packages..
from . import queries  # noqa: F401
from . import base  # noqa: F401
from . import help  # noqa: F401
from . import start  # noqa: F401
from . import menu  # noqa: F401
from . import reports  # noqa: F401

from .routers import users_router, subed_users_router

dp.include_router(users_router)
dp.include_router(subed_users_router)
