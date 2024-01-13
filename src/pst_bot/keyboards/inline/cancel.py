from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callback_data import SpamData

keyboard_buttons_questions = (
	(
		InlineKeyboardButton(text='Подтвердить', callback_data=SpamData(data='accept_send_all').pack()),
		InlineKeyboardButton(text='Отменить', callback_data=SpamData(data='cancel_send_all').pack()),
	),
)

keyboard_question_dialog = InlineKeyboardMarkup(
	inline_keyboard=keyboard_buttons_questions,
	one_time_keyboard=True,
)


keyboard_button_cancel = (
	(
		keyboard_buttons_questions[0][1],
	),
)

keyboard_cancel_dialog = InlineKeyboardMarkup(
	inline_keyboard=keyboard_button_cancel,
	one_time_keyboard=True,
)
