from __future__ import annotations

from typing import TYPE_CHECKING

# from aiogram import F
# from aiogram.fsm.storage.base import StorageKey
from filters import CommandTrigger

# from utils.misc.throttling import rate_limit
from .routers import admins_router

if TYPE_CHECKING:
	# from logging import Logger

	# from aiogram import Bot
	# from aiogram.filters import CommandObject
	from aiogram.types import Message
