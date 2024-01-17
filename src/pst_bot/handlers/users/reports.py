from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F

if TYPE_CHECKING:
	from aiogram import Bot
	from aiogram.filters import CommandObject
	from aiogram.types import Message

from filters import CommandUse
from texts import cmd_report_success_text

# from utils.misc.throttling import rate_limit
from utils.notify_admins import report_notify

from .routers import users_router


# TODO: Move filters..
@users_router.message(
	CommandUse(
		'report',
		magic4usage=~F.args.strip() | (F.args.strip().len() < 16),
		usage_text='Minimal length for report text 16 symblos & cooldown 10 mins.',
	),
)
# @rate_limit(600, 'report')
async def admins_report(message: Message, command: CommandObject, bot: Bot):
	# TODO: More user info..
	# TODO: FSM like too..
	report_form = f'user_id=`{message.from_user.id}`\nusername=`@{message.from_user.username}`\n\n{command.args}'
	await report_notify(bot, report_form)
	await message.answer(cmd_report_success_text)
