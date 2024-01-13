from __future__ import annotations

# TODO: Make it optional by looking to deps..
from .custom_model import CallbackB_ZSData

# from aiogram.filters.callback_data import CallbackData as CallbackB_ZSData


class VoiceData(CallbackB_ZSData, prefix='voice_data'):  # type: ignore
	name: str
