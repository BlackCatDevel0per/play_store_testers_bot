from __future__ import annotations

# from texts import cmd_start_hi_text, cmd_start_text
from typing import TYPE_CHECKING

from aiogram.filters import CommandStart

from .routers import users_router

# from utils.misc.throttling import rate_limit

if TYPE_CHECKING:
	from typing import Final

	from aiogram import Bot
	from aiogram.types import Message, User

	from utils.db import DB


@users_router.message(CommandStart())
# @rate_limit(60, 'start')
async def command_start(message: Message, db: DB, bot: Bot) -> None:
	BOT_SELF: Final[User] = await bot.me()
	await message.answer(
		(  # noqa: UP031
			'Привет %s!'
			'\n'
			'Это %s'
			'\n'
		) % (message.from_user.full_name, BOT_SELF.full_name),
	)

	#
	await db.tg_users.add_user(
		message.from_user.id, message.from_user.username,
		message.from_user.full_name, message.from_user.language_code,
	)

	# TODO: Unite & make checking methods..
	async with db._session_factory() as session:
		if not await db.apps._is_user_profile_exist(session, message.from_user.id):
			await db.apps.add_profile_options(
				user_id=message.from_user.id, gmails='',
			)
