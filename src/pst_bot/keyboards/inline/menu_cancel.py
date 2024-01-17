from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callback_data import MenuData

keyboard_menu_buttons_questions = (
	(
		InlineKeyboardButton(text='Подтвердить', callback_data=MenuData(action='confirm').pack()),
		InlineKeyboardButton(text='Отменить', callback_data=MenuData(action='cancel').pack()),
	),
)

keyboard_menu_question_dialog = InlineKeyboardMarkup(
	inline_keyboard=keyboard_menu_buttons_questions,
	one_time_keyboard=True,
)


keyboard_button_cancel = (
	(
		keyboard_menu_buttons_questions[0][1],
	),
)

keyboard_cancel_dialog = InlineKeyboardMarkup(
	inline_keyboard=keyboard_button_cancel,
	one_time_keyboard=True,
)
