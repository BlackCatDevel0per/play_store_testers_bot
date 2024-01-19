from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F
from aiogram.filters import CommandObject, StateFilter

from filters import CommandTrigger, CommandUse, filter_message_invalid_command_args4gen
from keyboards.inline import keyboard_menu

from .routers import users_router

if TYPE_CHECKING:
	# from logging import Logger

	from aiogram.fsm.context import FSMContext
	from aiogram.types import Message

	from utils.db import DB

# TODO: Ping bot..?


@users_router.message(
	CommandUse(
		'set_gmails',
		magic4usage=~F.args.strip() | (F.args.strip().len() < 13),
		usage_text_template=(
			'Использование: {prefix}{{command}} "почты аккаунтов через `,`"'
			'\n'
			'Вы ввели: {{command_args}}\n{usage_text}'
		),
		usage_text='Пожалуйста укажите хоть одну почту, минимум 13 символов, пример: some@gmail.com',
	),
)
async def set_gmail_command(message: Message, command: CommandObject, db: DB):
	##
	await db.apps.update_profile_options(
		search_properties={'user_id': message.from_user.id},
		# TODO: regex check..
		update_cols={'gmails': command.args},
	)
	await message.answer(f'Адреса: {command.args}\nУспешно добавлены')


# FIXME: Less duplicate & internatialization..
@users_router.message(CommandTrigger('menu'))
async def menu_command(message: Message):
	await message.answer('Выберите действие:', reply_markup=keyboard_menu)
