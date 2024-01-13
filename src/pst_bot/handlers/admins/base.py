from __future__ import annotations

from typing import TYPE_CHECKING

# from aiogram import F
# from aiogram.fsm.storage.base import StorageKey
from filters import CommandTrigger

from utils.core import sb

# from utils.misc.throttling import rate_limit
from .routers import admins_router

if TYPE_CHECKING:
	# from logging import Logger

	# from aiogram import Bot
	# from aiogram.filters import CommandObject
	from aiogram.types import Message


# TODO: Ты шо мне кидаешь?


@admins_router.message(CommandTrigger('status'))
# @rate_limit(5, 'status')
async def status(message: Message) -> None:
	...
	await message.answer(
		(
			f'Статус: {...}'
			'\n'
			'Ещё не сделано :/'
		),
	)


# TODO: Self recover (if was on).. & hash some data (like users ids) in db..
@admins_router.message(CommandTrigger('online'))
# @rate_limit(5, 'online')
async def online(message: Message) -> None:
	if not sb.is_polling:
		await sb.setup()
		await message.answer('Автоонлайн включён!')
		return
	await message.answer('Автоонлайн уже запущен..')


@admins_router.message(CommandTrigger('offline'))
# @rate_limit(5, 'offline')
async def offline(message: Message) -> None:
	if sb.is_polling:
		await sb.stop_polling()
		await message.answer('Автоонлайн отключён..')
		return
	await message.answer('Автоонлайн не запущен')
