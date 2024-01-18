from __future__ import annotations

from typing import TYPE_CHECKING

from data.config import ADMINS

if TYPE_CHECKING:
	from aiogram import Bot

from aiogram.types import BotCommand, BotCommandScopeChat

from utils import multiple_requests


async def wrap_set_bot_commands_for(user_id: int, bot: Bot, commands: list[BotCommand]) -> None:
	await bot.set_my_commands(
		commands=commands,
		scope=BotCommandScopeChat(chat_id=user_id),
	)


# exexexe XD
async def set_bot_commands(bot: Bot):
	# TODO: Clean & manage palettes..
	# set_bot_users_commands
	default_commands = [
		BotCommand(command='start', description='Запуск Бота'),
		BotCommand(command='help', description='Помощь'),

		BotCommand(command='set_gmails', description='Добавить gmail адреса почты'),
		BotCommand(command='menu', description='Меню действий'),
	]
	_admin_prefix = '[A]'
	##
	# set_bot_admins_commands
	# TODO: Inhetirate `BotCommand` with my text properties/prefixes.. Or at least use lambda..
	admin_commands = [
		*default_commands,
		# actions
		BotCommand(command='sh', description=f'{_admin_prefix} Выполнить shell-команду на сервере =)'),
		BotCommand(command='msg_all', description=f'{_admin_prefix} Массовая рассылка (спам)'),
		# info
		BotCommand(command='hardinfo', description=f'{_admin_prefix} Инфа о текущей нагрузке сервера (пока хреновый вывод..)'),
		# BotCommand(command='statistics', description=f'{_admin_prefix} Статистика бота (кол-во пользователей)'),

	]
	await bot.set_my_commands(default_commands)

	# TODO: Mb handle in errors handler..?
	# aiogram.exceptions.TelegramBadRequest: Telegram server says - Bad Request: chat not found
	await multiple_requests(
		wrap_set_bot_commands_for, users_ids=ADMINS, log_prefix='[Update Commands Scope]',
		bot=bot, commands=admin_commands,
	)
