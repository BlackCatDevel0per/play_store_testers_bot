from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F

from handlers.users.routers import users_router
from keyboards.inline import keyboard_menu_question_dialog
from states import FSMNewTicket

if TYPE_CHECKING:
	from logging import Logger
	from typing import Any

	from aiogram import Bot
	from aiogram.fsm.context import FSMContext
	from aiogram.fsm.state import State
	from aiogram.types import Message

	from utils.db import DB

# TODO: Info package & list all users gmails by steps..? (mb better just export to sheet..)

# TODO: One step back & cancel && default FSM methods constructor like these two


async def ticket_handle_state(
	message: Message,
	state: FSMContext,
	logger: Logger,

	#
	state_action: str,
	#
	current_state_data: dict[str, Any],
	next_state: State | None,
) -> None:
	logger.info(
		'User `%s` set %s: "%s"',
		message.from_user.username, state_action, message.text,
	)
	#
	await state.update_data(current_state_data)
	await state.set_state(next_state)


@users_router.message(FSMNewTicket.set_app_name)
async def ticket_handle_app_name(message: Message, state: FSMContext, logger: Logger) -> None:
	await ticket_handle_state(
		message, state, logger,

		'app name',
		current_state_data={'app_name': message.text},
		next_state=FSMNewTicket.set_description,
	)
	await message.answer('Введите описание:')


@users_router.message(FSMNewTicket.set_description)
async def ticket_handle_description(message: Message, state: FSMContext, logger: Logger) -> None:
	await ticket_handle_state(
		message, state, logger,

		'description',
		current_state_data={'description': message.text},
		next_state=FSMNewTicket.set_app_url,
	)
	await message.answer('Введите ссылку на приложение в Google Play:')  #


@users_router.message(FSMNewTicket.set_app_url)
async def ticket_handle_app_url(
	message: Message,
	state: FSMContext, logger: Logger,
) -> None:
	# TODO: Where better to check ticket existent..? (better look/refactor project architecture..)
	await ticket_handle_state(
		message, state, logger,

		'app url',
		current_state_data={'app_url': message.text},
		next_state=FSMNewTicket.confirm,
	)

	data = await state.get_data()

	# TODO: Remove old messages..
	# TODO: MD Format
	await message.answer(
		'Данные тикета:'
		'\n'
		f"Название: {data['app_name']}"
		'\n'
		'Описание:'
		'\n***\n'
		f"{data['description']}"
		'\n***\n'
		f"Ссылка на приложение: {data['app_url']}",
		reply_markup=keyboard_menu_question_dialog,  # TODO: Confirm inline markup..
	)
