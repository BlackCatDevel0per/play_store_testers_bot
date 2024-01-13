# from aiogram import types
# from aiogram.dispatcher.filters import Text as TextFilter

# from loader import bot, dp


# @dp.callback_query_handler(TextFilter(startswith="segment_"))
# async def process_callback_button_segment(callback_query: types.CallbackQuery):
# 	await bot.answer_callback_query(callback_query.id, cache_time=20)
# 	# Удаление кнопки (пока без cooldown)
# 	# delete reply markup ..
# 	await bot.edit_message_reply_markup(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id, reply_markup=None)
# 	...
