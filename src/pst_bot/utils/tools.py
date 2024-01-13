from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramBadRequest as aiogram_TelegramBadRequest
from aiogram.exceptions import TelegramForbiddenError as aiogram_TelegramForbiddenError

if TYPE_CHECKING:
	from collections.abc import Awaitable, Callable
	from typing import Any

	# TODO: Make & move into annotations package..
	AsyncFunc_with_args = Callable[[...], Awaitable[Any]]


logger = logging.getLogger('bot')


# UwU
async def multiple_requests(
	async_func: AsyncFunc_with_args, *,
	user_ids: list[int], prefix: str | None = None,
	**kwargs: Any,
) -> int:
	# NOTE: If you want use generators, make the second counter (instead of the length of the list) and count up on each exception.
	# FIXME: Length of prefix..?
	if not prefix:
		prefix = f'[{async_func.__module__}.{async_func.__name__}]'
	user_ids_count: int = len(user_ids)
	sent_requests_count = 0
	for user_id in user_ids:
		try:
			# Should be there (not in error handlers), because on exception all noncomplete stuff will drop..
			await async_func(user_id, **kwargs)
			sent_requests_count += 1
		except aiogram_TelegramBadRequest as ate:  # noqa: PERF203 (because bot api not allows so fast messaging)
			# TODO: More info.. (mb some requests to db..)
			logger.warning('%s Notify for `user_id=%i` error, because: %s', prefix, user_id, ate.message)
		except aiogram_TelegramForbiddenError as atfe:
			# TODO: More info..
			logger.warning('%s Notify for `user_id=%i` error, because: %s', prefix, user_id, atfe.message)
		except Exception as err:
			logger.exception('Sending to %i error args: %s', user_id, err.args)
	logger.info('%s Successfully sent: %i/%i', prefix, sent_requests_count, user_ids_count)
	return sent_requests_count
