from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from data.config import ADMINS
from utils.db.crud_queries import (
	query__users__user_id,
	query_count__users__users_ids,
)
from utils.db.cruds import DBApp
from utils.db.tables import UsersTable

if TYPE_CHECKING:
	from sqlalchemy import Column
	from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Split to groups
# TODO: Mb `finally` block..


class DBTGBase(DBApp):
	# TODO: Use this class to just unite access to db data levels..

	##
	async def _is_user_exist(self: DBTGBase, session: AsyncSession, user_id: int) -> bool:
		# TODO: Do it other way..
		query_user_id = query__users__user_id.where(UsersTable.user_id == user_id)
		fetch: int | None = await self.db._session_execute_fetch_one_or_none(session, query_user_id)
		del query_user_id
		if fetch:
			del fetch
			return True
		del fetch
		return False


	async def add_user(
		self: DBTGBase, user_id: int, username: str | None = None, full_name: str | None = None,
		language_code: str | None = None,
	) -> bool:
		try:
			user = UsersTable(
				user_id=user_id, username=username,
				full_name=full_name, language_code=language_code,
			)

			async with self.db._session_factory() as session:
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


	@property##
	def get_admins_count(self: DBTGBase) -> int:
		return len(ADMINS)  ##


	def _remove_admins_from_result(self: DBTGBase, data: list[int]) -> bool:
		for admin in ADMINS:
			data.remove(admin)
		return True


	async def get_users_ids(
		self: DBTGBase, *,
		no_admins: bool = False,
		FetchOne: bool = False,
	) -> list[Column] | list:##fo
		async with self.db._session_factory() as session:
			res = [i[0] for i in await self.db.select_cols_from(session, [UsersTable.user_id], FetchOne=FetchOne)]##
			if no_admins:
				self._remove_admins_from_result(res)
			return res


	# mb need count function in crud class..
	async def get_users_count(self: DBTGBase, *, no_admins: bool = False) -> int:
		async with self.db._session_factory() as session:
			fetch: int = await self.db._session_execute_fetch_one_or_none(
				session, query_count__users__users_ids,
			)
			if no_admins:
				admins_cnt = self.get_admins_count
				fetch -= admins_cnt  # lol if it becomes negative XD
				del admins_cnt
			return fetch
