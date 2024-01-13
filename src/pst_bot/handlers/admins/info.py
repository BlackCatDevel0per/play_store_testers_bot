from __future__ import annotations

from typing import TYPE_CHECKING

import psutil

from filters import CommandTrigger
# from filters import CommandTrigger, CommandUse

# from utils.misc.throttling import rate_limit
from .routers import admins_router

if TYPE_CHECKING:
	from aiogram.types import Message

	# from utils.db import DB


@admins_router.message(CommandTrigger('hardinfo'))
# @rate_limit(5, 'hardinfo')
async def hardinfo(message: Message):
	try:
		total_ram = int(psutil.virtual_memory()[0] / 1024**2)
		used_ram = int(psutil.virtual_memory()[3] / 1024**2)
		# free_ram = int(psutil.virtual_memory()[4]/1024)
		cpu_usage = psutil.cpu_percent(4)
		await message.answer(f'#### STATISTICS ####\
			\n\nCPU: {cpu_usage}%\
			\nRAM: {used_ram}/{total_ram} MB.'[:4096])
	except Exception as e:
		await message.answer(f'### CONSOLE ERROR ###\n\n{e}')


# @admins_router.message(CommandUsage('userinfo', usage_text='...'))
# # @rate_limit(5, 'userinfo')
# async def userinfo(message: Message):
# 	try:
# 		args = message.get_args()
# 		if not args:
# 			await message.answer("Дайте username или user_id")
# 			return
# 		user_nm_or_id = args
# 		search_limit: 'Union[int, str]' = 300
# 		if not isinstance(args, str):
# 			user_nm_or_id = args[0]
# 			search_limit = args[1]
# 			if search_limit.isnumeric():
# 				search_limit = int(search_limit)
# 		if user_nm_or_id.isnumeric():
# 			# get updates can be used for statistics of active users =)
# 			# updates = await bot.get_updates(limit=search_limit, allowed_updates=['message'], timeout=30)
# 			user_data = await UAPI().get_profile_from_user(int(user_nm_or_id))
# 		elif ' ' not in args:
# 			user_data = await UAPI().get_profile_from_user(user_nm_or_id)
# 		else:
# 			await message.answer("Дайте username или user_id")
# 		# cache_time =)
# 		await message.answer(
# 			f"Данные пользователя: {user_data.username} {user_data.first_name} {user_data.last_name if user_data.last_name else ''} {user_data.lang_code if user_data.lang_code else ''}")
# 	except Exception as e:
# 		await message.answer(f"### CONSOLE ERROR ###\n\n{e}")


# @admins_router.message(CommandTrigger('statistics'))
# # @rate_limit(5, 'statistics')
# async def statistics(message: Message, db: DB):
# 	try:
# 		# updates = await bot.get_updates(limit=search_limit, allowed_updates=['message'], timeout=30)
# 		await message.answer(f'Количество пользователей в бд: {await db.get_users_count()}')
# 	except Exception as e:
# 		await message.answer(f'### CONSOLE ERROR ###\n\n{e}')
