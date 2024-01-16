from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import MetaData, text

from .cruds import DBApp
from .tables import Base, UsersDataTable

if TYPE_CHECKING:
	from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!


class DBTriggers(DBApp):


	async def engine_create_UsersData_on_User_insert_trigger(
		self: DBTriggers, session: AsyncSession,
	) -> bool:  # noqa: N802
		# FIXME: Crutch, but ok..
		##
		stmt = text(
			(  # noqa: UP032
				"CREATE TRIGGER users_data_insert_trigger\n"
				"AFTER INSERT\n"
				"ON users\n"
				"BEGIN\n"
				"	INSERT INTO users_data (user_id, current_language_code)\n"
				"	VALUES (new.user_id, '{default_current_language_code}');\n"
				"END;"
			).format(
					default_current_language_code=UsersDataTable.current_language_code.default.arg,
			),
		)

		await session.execute(stmt)
		return True


	async def engine_create_AppsTesters_on_Dev_delete_trigger(
		self: DBTriggers, session: AsyncSession,
	) -> bool:  # noqa: N802
		# FIXME: Crutch, but ok..
		##
		stmt = text(
			'CREATE TRIGGER apps_tickets_delete_trigger\n'
			'AFTER DELETE\n'
			'ON apps_tickets\n'
			'BEGIN\n'
			'	DELETE FROM apps_testers_data\n'
			'	WHERE ticket_id = OLD.id;\n'
			'END;'
		)

		await session.execute(stmt)
		return True


	async def engine_create_all(self: DBTriggers, metadata: MetaData = Base.metadata) -> bool:
		##
		ret = await self.db.engine_create_all(metadata)
		async with self.db._session_factory() as session:
			await self.engine_create_UsersData_on_User_insert_trigger(session)
			await self.engine_create_AppsTesters_on_Dev_delete_trigger(session)
			await session.commit()
		return ret
