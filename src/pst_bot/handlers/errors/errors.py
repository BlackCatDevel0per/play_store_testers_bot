from __future__ import annotations

from typing import TYPE_CHECKING

# from aiogram.exceptions import CantParseEntities, MessageNotModified, TelegramAPIError
from aiogram import F

# from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramForbiddenError
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter

# from aiogram.methods import AnswerCallbackQuery, AnswerInlineQuery
from aiogram.methods import AnswerInlineQuery

# Because logger now only in inner middleware..
from utils.misc.logging import logger

from .routers import errors_router

if TYPE_CHECKING:
	from aiogram.types import ErrorEvent


# TODO: More errors handlers..?
# TODO: Dataobjects as enums..
# TODO: Type hints..
@errors_router.error(
	ExceptionTypeFilter(TelegramBadRequest),
	(F.exception.message == 'Bad Request: query is too old and response timeout expired or query ID is invalid')
	&
	F.exception.method.func(lambda method: isinstance(method, AnswerInlineQuery)),
)
async def too_old_query_error_handler(event: ErrorEvent) -> None:
	event.exception: TelegramBadRequest
	event.exception.method: AnswerInlineQuery
	logger.error('Too old query with method `%s` (or invalid query id)', repr(event.exception.method))


@errors_router.errors(
	ExceptionTypeFilter(TelegramBadRequest),
	(F.exception.message == 'Bad Request: chat not found'),
)
async def chat_not_found_errors_handler(event: ErrorEvent) -> None:
	event.exception: TelegramBadRequest
	logger.error('Chat not found for request method `%s`', repr(event.exception.method))

# TODO: Handle parsing..
# TODO: Handle other api errors..
