from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import CHANNELS_LINKS

keyboard_buttons_channels_links_links = (
	tuple(InlineKeyboardButton(text=name, url=link) for name, link in CHANNELS_LINKS.items()),
)
keyboard_channels_links_list = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons_channels_links_links, resize_keyboard=True)
