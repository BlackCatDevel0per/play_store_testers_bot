from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from texts import btn_text_back

keyboard_buttons = (
	(
		KeyboardButton(text=btn_text_back),
	),
)

keyboard = ReplyKeyboardMarkup(
	keyboard=keyboard_buttons,
	resize_keyboard=True,
)
