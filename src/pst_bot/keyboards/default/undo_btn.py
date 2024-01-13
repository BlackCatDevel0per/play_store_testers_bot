from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from texts import text_undo

keyboard_buttons = (
	(
		KeyboardButton(text=text_undo),
	),
)

keyboard = ReplyKeyboardMarkup(
	keyboard=keyboard_buttons,
	resize_keyboard=True,
)
