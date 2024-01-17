from __future__ import annotations

import asyncio
import shlex
from typing import TYPE_CHECKING

# from aiogram import F
# from aiogram.filters import StateFilter
# from aiogram.fsm.storage.base import StorageKey

from filters import CommandUse
# from filters import CommandTrigger, CommandUse
# from keyboards.callback_data import SpamData
# from keyboards.inline import keyboard_cancel_dialog, keyboard_question_dialog
# from states import FSMAdminsMessagingAccept

# from utils.misc.throttling import rate_limit
# from utils.notify_admins import msg_to

from .routers import admins_router

if TYPE_CHECKING:
	# from logging import Logger

	# from aiogram import Bot
	from aiogram.filters import CommandObject
	# from aiogram.fsm.context import FSMContext
	from aiogram.types import Message
	# from aiogram.types import CallbackQuery, Message

	# from utils.db import DB

# Callback


@admins_router.message(CommandUse('sh', usage_text='Paste shell command to args.'))
# @rate_limit(5, 'sh')
async def shell(message: Message, command: CommandObject) -> None:
	try:
		process = await asyncio.create_subprocess_exec(*shlex.split(command.args), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
		stdout, stderr = await process.communicate()
		command_output = f'{stdout.decode().strip()}\n{stderr.decode().strip()}'.strip()
		await message.answer(f'#### CONSOLE ####\n\n{command_output}'[:4096])
	except Exception as e:
		await message.answer(f'### CONSOLE ERROR ###\n\n{e}')


# TODO: Admins for admins notifications & quick switch packages.. (mv from conf file..) 


# @admins_router.message(CommandTrigger('msg_all'))
# # @rate_limit(5, 'msg_all')
# async def message_all_wait_msg(message: Message, bot: Bot, state: FSMContext) -> None:
# 	# try:
# 	wait_msg = await message.answer('Отправьте сообщение:', reply_markup=keyboard_cancel_dialog)  # mb need autoremove..
# 	await state.storage.set_data(
# 		StorageKey(bot_id=bot.id, user_id=message.from_user.id, chat_id=message.chat.id),
# 		data={'wait_msg': wait_msg},
# 	)  # FIXME: CHECKME..
# 	await state.set_state(FSMAdminsMessagingAccept.message)
# 	# except Exception as e:
# 	# 	# TODO: Callstack..
# 	# 	await message.answer(f'### CONSOLE ERROR ###\n\n{e}')


# @admins_router.callback_query(SpamData.filter(F.data == 'cancel_send_all'), StateFilter(FSMAdminsMessagingAccept))#
# async def message_all_cancel(callback_query: CallbackQuery, bot: Bot, state: FSMContext, logger: Logger) -> None:
# 	try:
# 		await bot.edit_message_text(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text='Отменено', reply_markup=None)
# 		await del_ac_msg(bot, callback_query, state)
# 		await state.clear()
# 	except Exception as e:
# 		logger.exception('Exception args: %s', e.args)


# async def del_ac_msg(bot: Bot, callback_query: CallbackQuery, state: FSMContext) -> None:
# 	data = await state.get_data()
# 	if 'ac_msg' in data:##
# 		ac_msg = data['ac_msg']
# 		# await ac_msg.delete()
# 		await bot.delete_message(message_id=ac_msg.message_id, chat_id=callback_query.message.chat.id)


# @admins_router.message(FSMAdminsMessagingAccept.message)
# async def message_all_wait_accept_send(message: Message, bot: Bot, state: FSMContext) -> None:
# 	try:
# 		data = await state.get_data()
# 		if 'wait_msg' in data:
# 			wait_msg: Message = data['wait_msg']
# 			ac_msg = await bot.edit_message_text(message_id=wait_msg.message_id, chat_id=wait_msg.chat.id, text=wait_msg.text, reply_markup=None)
# 		await state.set_data({'ac_msg': ac_msg, 'msg': message})
# 		await message.answer('Подтвердите действие:', reply_markup=keyboard_question_dialog)
# 		await state.set_state(FSMAdminsMessagingAccept.accept_and_continue)
# 	except Exception as e:
# 		await message.answer(f'### CONSOLE ERROR ###\n\n{e}')


# @admins_router.callback_query(SpamData.filter(F.data == 'accept_send_all'), FSMAdminsMessagingAccept.accept_and_continue)
# async def message_all(callback_query: CallbackQuery, bot: Bot, state: FSMContext, db: DB, logger: Logger):
# 	try:
# 		# mb need some progress show..
# 		sending_msg = await bot.edit_message_text(
# 			message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, text='Отправка..', reply_markup=None,
# 		)
# 		await del_ac_msg(bot, callback_query, state)
# 		data = await state.get_data()
# 		msg: Message = data['msg']
# 		# user_ids = db.get_users_ids(no_admins=True)
# 		user_ids = await db.get_users_ids()
# 		sended_cnt = await msg_to(msg, user_ids, logger)
# 		await sending_msg.delete()
# 		await msg.reply(f'Отправлено: {sended_cnt}/{await db.get_users_count(no_admins=True)} пользователям =)', reply_markup=None)
# 		await state.clear()
# 	except Exception as e:
# 		await msg.answer(f'### CONSOLE ERROR ###\n\n{e}')
