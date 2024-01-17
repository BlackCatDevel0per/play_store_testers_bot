from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F

from handlers.users.routers import users_router
from keyboards.callback_data import MenuData
from states import FSMNewTicket

# TODO: Move into the other package..
from utils.db.apps_interact import TicketDuplicationError

if TYPE_CHECKING:
	from logging import Logger

	from aiogram import Bot
	from aiogram.fsm.context import FSMContext
	from aiogram.types import CallbackQuery, Message

	from utils.db import DB

# TODO: One step back & cancel && default FSM methods constructor like these two


# TODO: Use enums for some filters data..?
@users_router.callback_query(MenuData.filter(F.action == 'new_ticket'))
async def handle_new_ticket(
	callback_query: CallbackQuery,
	bot: Bot, state: FSMContext,
	logger: Logger,
) -> None:
	logger.info("User `%s` select action: '%s'", callback_query.from_user.username, 'new_ticket')
	await state.set_state(FSMNewTicket.set_app_name)
	await bot.send_message(callback_query.from_user.id, 'Введите название приложения:')

	await callback_query.answer()


@users_router.callback_query(FSMNewTicket.confirm, MenuData.filter(F.action == 'confirm'))
async def ticket_handle_confirm(
	callback_query: CallbackQuery,
	bot: Bot, state: FSMContext, db: DB, logger: Logger,
) -> None:
	data = await state.get_data()
	try:
		await db.apps.add_ticket(
			callback_query.from_user.id, callback_query.from_user.username,
			**data,
		)
	except TicketDuplicationError:
		#
		await bot.send_message(
			callback_query.from_user.id,
			'Тикет с такой ссылкой уже существует!\nНачните заново..',
		)
		await state.clear()
		return

	logger.info(
		'New Ticket of dev `%s` successfully added!',
		callback_query.from_user.username,
	)

	# TODO: Message all (exclude owner of ticket)

	await bot.send_message(callback_query.from_user.id, 'Готово =)')

	await state.clear()

	await callback_query.answer()


# TODO: Same action for command..
@users_router.callback_query(FSMNewTicket, MenuData.filter(F.action == 'cancel'))
async def ticket_handle_cancel(
	callback_query: CallbackQuery,
	bot: Bot, state: FSMContext, logger: Logger,
) -> None:
	# TODO: Clean markups..
	await state.clear()
	logger.info('User `%s` cancelled adding new ticket..', callback_query.from_user.username)
	await bot.send_message(callback_query.from_user.id, 'Отменено')

	await callback_query.answer()


# @users_router.callback_query(MenuData.filter(F.data == 'get_tickets'))
