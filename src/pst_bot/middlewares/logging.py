from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import BaseMiddleware

from utils.misc.logging import logger

if TYPE_CHECKING:
	from collections.abc import Awaitable, Callable
	from logging import Logger
	from typing import Any

	from aiogram.types import TelegramObject


# TODO: Rich..
class LoggingMiddleware(BaseMiddleware):
	"""Logging middleware."""

	def __init__(self, logger: Logger = logger) -> None:
		self.logger = logger


	async def __call__(
		self: LoggingMiddleware,
		handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
		event: TelegramObject,
		data: dict[str, Any],
	) -> Any:
		data['logger'] = self.logger
		return await handler(event, data)
