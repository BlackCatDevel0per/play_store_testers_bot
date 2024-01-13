from __future__ import annotations

# from texts import cmd_start_hi_text, cmd_start_text
from typing import TYPE_CHECKING

from aiogram.filters import CommandStart

from .routers import admins_router

# from utils.misc.throttling import rate_limit

if TYPE_CHECKING:
	from typing import Final

	from aiogram import Bot
	from aiogram.types import Message, User

	from utils.db import DB


@admins_router.message(CommandStart())
# @rate_limit(60, 'start')
async def command_start(message: Message, db: DB, bot: Bot) -> None:
	BOT_SELF: Final[User] = await bot.me()
	await message.answer(
		(  # noqa: UP031
			'Приветствую повелитель %s'
			'\n'
			'Обращайтесь ко мне по ~имени %s'
			'\n'
		) % (message.from_user.full_name, BOT_SELF.full_name),
	)
