from __future__ import annotations

from typing import TYPE_CHECKING

from data.config import ADMINS
from texts import (
	shutdown_notify_admins_text,
	startup_notify_admins_text,
	user_report_notify_admins_text,
)

from .tools import multiple_requests

if TYPE_CHECKING:
	from logging import Logger

	from aiogram import Bot
	from aiogram.types import Message

# TODO: Mb add tasking to faster spam if bot has much administrators.. Lol telegram will kick it XD


# UwU
async def notify(bot: Bot, text: str, *, user_ids: list[int]) -> None:
	await multiple_requests(bot.send_message, user_ids=user_ids, prefix='[Admins notify]', text=text)


async def on_startup_notify(bot: Bot, logger: Logger) -> None:
	await notify(bot, startup_notify_admins_text, user_ids=ADMINS)
	logger.info('Bot is running!')


async def on_shutdown_notify(bot: Bot, logger: Logger) -> None:
	await notify(bot, shutdown_notify_admins_text, user_ids=ADMINS)
	logger.info('Shuting down bot..')


async def report_notify(bot: Bot, text: str) -> None:
	await notify(bot, f"{user_report_notify_admins_text}\n{text}", user_ids=ADMINS)


# Pls move to other file
# Need some aiogram types..
# Not arg isn't iterable now..
async def msg_to(msg: Message, user_ids: list[int], logger: Logger) -> int:
	"""Can send almost all messages with different content types.

	Usually used for spamming =)
	"""
	logger.info('Spamming..')
	return await multiple_requests(
		# TODO: Use other func.. & use bot from message or bot from args (mb optional) or at least `msg._bot`!
		msg.copy_to, user_ids=user_ids, prefix='[SPAM]',
	)
