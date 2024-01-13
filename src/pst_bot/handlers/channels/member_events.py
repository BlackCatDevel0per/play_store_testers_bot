from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import F
from aiogram.enums import ChatType
from aiogram.filters.chat_member_updated import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter

from data.config import CHANNELS_IDS

from .routers import channels_router

if TYPE_CHECKING:
	from logging import Logger

	from aiogram.types import ChatMemberUpdated

	from utils.db import DB


# TODO: Mb move to other level (out of antiflood/throttling middleware..?)
# TODO: Check if it's first time or not..
# TODO: Filter channels by ..
@channels_router.chat_member(
	ChatMemberUpdatedFilter(
		member_status_changed=IS_NOT_MEMBER >> IS_MEMBER,
	),
	# FIXME: Move to 2 filters..
	(F.chat.type == ChatType.CHANNEL) & F.chat.id.in_(CHANNELS_IDS),
)
async def join_member_event_handler(event: ChatMemberUpdated, db: DB, logger: Logger) -> None:
	await db.add_channel_subscription(event.from_user.id, event.chat.id)
	logger.info(
		'Пользователь `%i`=`%s` подписался на канал `%s`=`%s`',
		event.from_user.id, event.from_user.username, event.chat.username, event.chat.title,
	)
	# TODO: Mb send message after subscribe..


@channels_router.chat_member(
	ChatMemberUpdatedFilter(
		member_status_changed=IS_MEMBER >> IS_NOT_MEMBER,
	),
	# FIXME: Move to 2 filters..
	(F.chat.type == ChatType.CHANNEL) & F.chat.id.in_(CHANNELS_IDS),
)
async def left_member_event_handler(event: ChatMemberUpdated, db: DB, logger: Logger) -> None:
	await db.del_channel_subscription(event.from_user.id, event.chat.id)
	logger.info(
		'Пользователь `%i`=`%s` отписался от канала `%s`=`%s`',
		event.from_user.id, event.from_user.username, event.chat.username, event.chat.title,
	)
