from __future__ import annotations

from typing import TYPE_CHECKING

from filters import CommandTrigger

if TYPE_CHECKING:
    from aiogram.types import Message

from .routers import admins_router

# from utils.misc.throttling import rate_limit


@admins_router.message(CommandTrigger('help'))
# @rate_limit(15, 'help')
async def command_help(message: Message):
    await message.answer('Пока всего пара команд и они в палетке/меню')
