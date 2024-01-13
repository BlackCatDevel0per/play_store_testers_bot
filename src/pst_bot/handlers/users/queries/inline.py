from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.exceptions import TelegramForbiddenError as aiogram_TelegramForbiddenError
from aiogram.types import (
	InlineQueryResultArticle,
	InlineQueryResultCachedAudio,
	InputTextMessageContent,
)
from filters import _endswith, filter_inline_empty_query_data, filter_inline_valid_query_data4gen

from utils.core import get_audio, upload_audio

if TYPE_CHECKING:
	from logging import Logger

	from aiogram import Bot
	from aiogram.types import InlineQuery

	from utils.db import DB

from handlers.users.routers import subed_users_router

endswith = ', '.join(f'"{i}"' for i in _endswith)


@subed_users_router.inline_query(filter_inline_empty_query_data)
# FIXME: Set another rate limit after implement flags..
async def invalid_query_text(query: InlineQuery, bot: Bot, db: DB) -> None:
	user_voice = await db.get_voice(query.from_user.id)
	# TODO.. In messages (filters) too.. (move to other query..)
	result = InlineQueryResultArticle(
		id='1',
		title=(
			f'Закончите предложение с `{endswith}`.'
			'\n'
			f'Ваш голос: `{user_voice}`'
			'\n'
			'Выбрать можно в лс!'
		),
		input_message_content=InputTextMessageContent(
			message_text=f'Закончите предложение с {endswith}',
		),
	)

	await bot.answer_inline_query(query.id, results=[result], cache_time=3)


# FIXME: Crutch (filter)
# TODO: Add filters and change logic..
# TODO: Set throttle options..
@subed_users_router.inline_query(filter_inline_valid_query_data4gen)
async def valid_query_data4gen(query: InlineQuery, bot: Bot, db: DB, logger: Logger) -> None:
	query_text = query.query.strip()
	user_voice = await db.get_voice(query.from_user.id)
	# TODO: Notify & do `Voice restored to default` if KeyError..
	audio_file = get_audio(user_voice, query_text)

	# Slow or not? Hmm..
	try:
		audio_id = await upload_audio(bot, query.from_user.id, audio_file, query_text)
	except aiogram_TelegramForbiddenError:
		# Forbidden: bot can't initiate conversation with a user
		# Forbidden: bot was blocked by the user

		# Need some other variants of this warning..
		result = InlineQueryResultArticle(
			id='1',
			title='Откройте личку с ботом и пропишите /start.',
			input_message_content=InputTextMessageContent(message_text='Личка с ботом не открыта!'),
		)
	except Exception as e:
		logger.critical('f*ck up! %s', e, exc_info=True)
		# TODO: Callback ~fatal error notification..
	else:##
		result = InlineQueryResultCachedAudio(
			id='1',
			audio_file_id=audio_id,
			caption=(
				f'Ваш голос: {user_voice}'
				'\n'
				'Выбрать можно в лс!'
			),
		)

	await bot.answer_inline_query(query.id, results=[result], cache_time=2)## Just 2 secs?
