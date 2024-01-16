from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import BaseMiddleware

from utils.db import DB

if TYPE_CHECKING:
	from collections.abc import Awaitable, Callable
	from typing import Any

	from aiogram.types import TelegramObject


# TODO: Session pool..
class DBMiddleware(BaseMiddleware):
	"""Simple middleware."""

	def __init__(self, *args: Any, **kwargs: Any) -> None:
		self.db = DB(*args, **kwargs)  # TODO: More configure..

	async def __call__(
		self: DBMiddleware,
		handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
		event: TelegramObject,
		data: dict[str, Any],
	) -> Any:
		data['db'] = self.db
		return await handler(event, data)
