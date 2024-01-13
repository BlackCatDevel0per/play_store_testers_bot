from __future__ import annotations

from .custom_model import CallbackB_ZSData

# from aiogram.filters.callback_data import CallbackData as CallbackB_ZSData


class SpamData(CallbackB_ZSData, prefix='admin-spam_data'):  # type: ignore
	data: str
