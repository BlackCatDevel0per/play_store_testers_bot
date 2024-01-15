from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select

from utils.db.cruds import DBApp
from utils.db.tables import (
	UsersChannelsSubscriptionsTable,
)

if TYPE_CHECKING:
	from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Mb `finally` block..


class DBChannelsSubscriptions(DBApp):


	async def add_channel_subscription(
		self: DBChannelsSubscriptions, user_id: int, channel_id: int,
	) -> bool:
		try:
			user_sub = UsersChannelsSubscriptionsTable(
				user_id=user_id, channel_id=channel_id,
			)

			async with self.db._session_factory() as session:
				# mb I can do this without list?
				if not await self.db.tg_users._is_user_exist(session, user_id):##
					logger.warning("User `%i` doesn't exists, channel_id=`%i`", user_id, channel_id)
					return False

				if await self._is_user_subscribed(session, user_id, channel_id):##
					logger.warning(
						"User `%i` already subscribed, channel_id=`%i`",
						user_id, channel_id,
					)
					return True

				session.add(user_sub)

				await session.flush()
				await session.commit()

				logger.info('User subscription `%i`=`%i` added', user_id, channel_id)

				return True

		except Exception:
			logger.exception('User subscription add with data `%s` failed!', user_sub)
			return False


	async def del_channel_subscription(
		self: DBChannelsSubscriptions,
		user_id: int, channel_id: int,
	) -> bool:
		try:
			async with self.db._session_factory() as session:
				# mb I can do this without list?
				if not await self.db.tg_users._is_user_exist(session, user_id):
					logger.warning("User `%i` doesn't exists, channel_id=`%i`", user_id, channel_id)
					return False

				if not await self._is_user_subscribed(session, user_id, channel_id):###
					logger.warning("User `%i` isn't subscribed yet, channel_id=`%i`", user_id, channel_id)
					return False

				stmt = (
					delete(UsersChannelsSubscriptionsTable)
					.where(
						UsersChannelsSubscriptionsTable.user_id == user_id,
						UsersChannelsSubscriptionsTable.channel_id == channel_id,
					)
				)  ##

				await session.execute(stmt)

				##
				await session.flush()
				await session.commit()

				logger.info('User subscription `%i`=`%i` deleted', user_id, channel_id)

				return True

		except Exception:
			logger.exception('User subscription delete with data `%i`=`%i` failed!', user_id, channel_id)
			return False


	async def _is_user_subscribed(
		self: DBChannelsSubscriptions,
		session: AsyncSession,
		user_id: int, channel_id: int,
	) -> bool:
		query_user_channels = (
			select(UsersChannelsSubscriptionsTable)
			.where(
				UsersChannelsSubscriptionsTable.user_id == user_id,
				UsersChannelsSubscriptionsTable.channel_id == channel_id,
			)
		)  ##
		return bool(await self.db._session_execute_fetch_one_or_none(session, query_user_channels))


	####
	async def is_user_subscribed(
		self: DBChannelsSubscriptions,
		user_id: int, channel_id: int,
	) -> bool:
		async with self.db._session_factory() as session:
			return await self._is_user_subscribed(session, user_id, channel_id)


	##
	async def is_user_subscribed_to(
		self: DBChannelsSubscriptions,
		user_id: int, channels_ids: tuple[int],
	) -> bool:
		##del..
		async with self.db._session_factory() as session:
			query_user_channels = (
				select(UsersChannelsSubscriptionsTable)
				.where(
					UsersChannelsSubscriptionsTable.user_id == user_id,
					UsersChannelsSubscriptionsTable.channel_id.in_(channels_ids),
				)
			)  ##
			res = (await session.execute(query_user_channels)).scalars().all()
			return bool(res) and len(res) == len(channels_ids)
