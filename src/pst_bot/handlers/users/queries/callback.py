from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F
from aiogram.filters import StateFilter

from handlers.users.routers import users_router
from keyboards.callback_data import MenuData
from states import FSMNewTicket

# TODO: Move into the other package..
from utils.db.apps_interact import TicketDuplicationError
from utils.tools import spam2users

if TYPE_CHECKING:
	from logging import Logger

	from aiogram import Bot
	from aiogram.fsm.context import FSMContext
	from aiogram.types import CallbackQuery, Message

	from utils.db import DB
	from utils.db.tables import AppsTicketsTable as AppTicket

# TODO: One step back & cancel && default FSM methods constructor like these two


# TODO: Use enums for some filters data..?
# TODO: Limit & ban spammers..
# TODO: Dynamically update tickets using inline button under message & get from that messageinfo about ticket..
# TODO: Make app_url column unique & other sql decorations..?
# TODO: Make normal README & spec..
@users_router.callback_query(StateFilter(None), MenuData.filter(F.action == 'new_ticket'))
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
		# TODO: Mb better return object..? Make method for it..
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

	# TODO: Store messages chat_id+message_id pairs to dynamically update it!
	# ticket_record: AppTicket = await db.apps.get_ticket_by({'app_url': data['app_url']})

	ticket: str = (  # TODO: Construct it part-by-part..
		f'username: @{callback_query.from_user.username}'
		'\n'
		f"Название: {data['app_name']}"
		'\n'
		'Описание:'
		'\n***\n'
		f"{data['description']}"
		'\n***\n'
		f"Ссылка на приложение: {data['app_url']}"
	)

	# TODO: Accepting keyboard & events with sending gmail to dev (aka ticket author)..

	await callback_query.message.edit_reply_markup(reply_markup=None)
	# TODO: Mb sending progress..
	spam_reply = await callback_query.message.reply('Рассылка..')

	# Spam to all excluding sender
	users_ids = await db.tg_users.get_users_ids()
	# TODO: Make option for users to exclude some testers (blacklist) & blacklist self too..
	# NOTE: Uncomment on prod..
	# for index, user_id in enumerate(users_ids):
	# 	if user_id == callback_query.from_user.id:
	# 		del users_ids[index]
	# 		break

	sent_count: int = await spam2users(bot, ticket, users_ids=users_ids)

	del users_ids

	# TODO: Cancel on-half.. & mb more spam control from dev (& user) side..
	# TODO: Show failed count..
	await spam_reply.edit_text(f'Готово =)\nОтправлено: {sent_count}')

	await state.clear()

	await callback_query.answer()


# TODO: Same action for command..
@users_router.callback_query(StateFilter(FSMNewTicket), MenuData.filter(F.action == 'cancel'))
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
