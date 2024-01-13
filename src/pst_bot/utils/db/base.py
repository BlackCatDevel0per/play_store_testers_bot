from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import Column, MetaData, delete, func, select, text, update

from data.config import ADMINS

from .crud_cache import (
	query__users__user_id,
	query_count__users__users_ids,
)
from .cruds import ComfortCRUD
from .tables import Base, UsersChannelsSubscriptionsTable, UsersDataTable, UsersTable

if TYPE_CHECKING:
	from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Split to groups
# TODO: Mb `finally` block..


class DB(ComfortCRUD):

	##
	async def _is_user_exist(self: DB, session: AsyncSession, user_id: int) -> bool:
		# mb need move to other func in parent class..
		# & need add @connection_required decorator
		# TODO: Do it other way..
		query_user_id = query__users__user_id.where(UsersTable.user_id == user_id)
		fetch: int | None = await self._session_execute_fetch_one_or_none(session, query_user_id)
		del query_user_id
		if fetch:
			del fetch
			return True
		del fetch
		return False


	async def engine_create_UsersData_on_User_insert_trigger(self: DB, session: AsyncSession) -> bool:  # noqa: N802
		# FIXME: Crutch, but ok..
		stmt = text(
			(  # noqa: UP032
			"CREATE TRIGGER users_data_insert_trigger\n"
			"AFTER INSERT\n"
			"ON users\n"
			"BEGIN\n"
			"	INSERT INTO users_data (user_id, current_language_code)\n"
			"	VALUES (new.user_id, '{default_current_language_code}');\n"
			"END;").format(
				default_current_language_code=UsersDataTable.current_language_code.default.arg,
			),
		)

		await session.execute(stmt)
		return True


	async def engine_create_all(self: DB, metadata: MetaData = Base.metadata) -> bool:
		ret = await super().engine_create_all(metadata)
		async with self._session_factory() as session:
			await self.engine_create_UsersData_on_User_insert_trigger(session)
			await session.commit()
		return ret


	async def add_user(
		self: DB, user_id: int, username: str | None = None, full_name: str | None = None,
		language_code: str | None = None,
	) -> bool:
		try:
			user = UsersTable(
				user_id=user_id, username=username,
				full_name=full_name, language_code=language_code,
			)

			async with self._session_factory() as session:
				# mb I can do this without list?
				if await self._is_user_exist(session, user_id):
					logger.info('User `%s` already exists', username)
					return True

				session.add(user)

				await session.flush()
				await session.commit()

				logger.info('User `%s` added', username)

				return True

		except Exception:
			logger.exception('User add with data `%s` failed!', user)
			return False


	async def add_channel_subscription(self: DB, user_id: int, channel_id: int) -> bool:
		try:
			user_sub = UsersChannelsSubscriptionsTable(
				user_id=user_id, channel_id=channel_id,
			)

			async with self._session_factory() as session:
				# mb I can do this without list?
				if not await self._is_user_exist(session, user_id):##
					logger.warning("User `%i` doesn't exists, channel_id=`%i`", user_id, channel_id)
					return False

				if await self._is_user_subscribed(session, user_id, channel_id):##
					logger.warning("User `%i` already subscribed, channel_id=`%i`", user_id, channel_id)
					return True

				session.add(user_sub)

				await session.flush()
				await session.commit()

				logger.info('User subscription `%i`=`%i` added', user_id, channel_id)

				return True

		except Exception:
			logger.exception('User subscription add with data `%i` failed!', user_sub)
			return False


	async def del_channel_subscription(self: DB, user_id: int, channel_id: int) -> bool:
		try:
			async with self._session_factory() as session:
				# mb I can do this without list?
				if not await self._is_user_exist(session, user_id):
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


	async def _is_user_subscribed(self: DB, session: AsyncSession, user_id: int, channel_id: int) -> bool:
		query_user_channels = (
			select(UsersChannelsSubscriptionsTable)
			.where(
				UsersChannelsSubscriptionsTable.user_id == user_id,
				UsersChannelsSubscriptionsTable.channel_id == channel_id,
			)
		)  ##
		return bool(await self._session_execute_fetch_one_or_none(session, query_user_channels))


	####
	async def is_user_subscribed(self: DB, user_id: int, channel_id: int) -> bool:
		async with self._session_factory() as session:
			return await self._is_user_subscribed(session, user_id, channel_id)


	##
	async def is_user_subscribed_to(self: DB, user_id: int, channels_ids: tuple[int]) -> bool:
		##del..
		async with self._session_factory() as session:
			query_user_channels = (
				select(UsersChannelsSubscriptionsTable)
				.where(
					UsersChannelsSubscriptionsTable.user_id == user_id,
					UsersChannelsSubscriptionsTable.channel_id.in_(channels_ids),
				)
			)  ##
			res = (await session.execute(query_user_channels)).scalars().all()
			return bool(res) and len(res) == len(channels_ids)


	@property##
	def get_admins_count(self: ComfortCRUD) -> int:
		return len(ADMINS)  ##


	def _remove_admins_from_result(self: DB, data: list[int]) -> bool:
		for admin in ADMINS:
			data.remove(admin)
		return True


	async def get_users_ids(self: DB, *, no_admins: bool = False, FetchOne: bool = False) -> list[Column] | list:##fo
		async with self._session_factory() as session:
			res = [i[0] for i in await self.select_cols_from(session, [UsersTable.user_id], FetchOne=FetchOne)]##
			if no_admins:
				self._remove_admins_from_result(res)
			return res


	# mb need count function in crud class..
	async def get_users_count(self: DB, *, no_admins: bool = False) -> int:
		async with self._session_factory() as session:
			fetch: int = await self._session_execute_fetch_one_or_none(session, query_count__users__users_ids)
			if no_admins:
				admins_cnt = self.get_admins_count
				fetch -= admins_cnt  # lol if it becomes negative XD
				del admins_cnt
			return fetch
