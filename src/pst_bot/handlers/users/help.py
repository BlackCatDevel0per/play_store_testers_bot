from __future__ import annotations

from typing import TYPE_CHECKING

from filters import CommandTrigger
from texts import cmd_help_text, feedback_text

if TYPE_CHECKING:
    from aiogram.types import Message

from .routers import users_router

# from utils.misc.throttling import rate_limit


@users_router.message(CommandTrigger('help'))
# @rate_limit(15, 'help')
async def command_help(message: Message):
    await message.answer(cmd_help_text)
