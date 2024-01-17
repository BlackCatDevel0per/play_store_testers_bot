from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.callback_data import MenuData

keyboard_buttons_menu = (
	(
		InlineKeyboardButton(text='Новый тикет', callback_data=MenuData(action='new_ticket').pack()),
		InlineKeyboardButton(text='Мои тикеты', callback_data=MenuData(action='get_tickets').pack()),
	),
)

keyboard_menu = InlineKeyboardMarkup(
	inline_keyboard=keyboard_buttons_menu,
	# one_time_keyboard=True,  ##
)
