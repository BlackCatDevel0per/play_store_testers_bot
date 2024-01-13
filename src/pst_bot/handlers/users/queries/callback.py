from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from aiogram.types import CallbackQuery

	from utils.db import DB

from keyboards.callback_data import VoiceData

from handlers.users.routers import subed_users_router


@subed_users_router.callback_query(VoiceData.filter())
async def handle_voice_choice(
	callback_query: CallbackQuery, callback_data: VoiceData,
	db: DB,
) -> None:
	await db.set_voice(callback_query.from_user.id, callback_data.name)
	await callback_query.answer(f'Вы выбрали: {callback_data.name}')
