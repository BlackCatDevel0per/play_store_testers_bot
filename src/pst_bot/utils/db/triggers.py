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
		stmt4sqlite = text(
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

		stmt_func = text(
			(  # noqa: UP032
				'CREATE OR REPLACE FUNCTION users_data_insert_function()\n'
				'RETURNS TRIGGER AS $$\n'
				'BEGIN\n'
				'	INSERT INTO users_data (user_id, current_language_code)\n'
				"	VALUES (NEW.user_id, '{default_current_language_code}');\n"
				'	RETURN NEW;\n'
				'END;\n'
				'$$ LANGUAGE plpgsql;'
			).format(
					default_current_language_code=UsersDataTable.current_language_code.default.arg,
			),
		)

		stmt_drop_if_exist = text(
			'DROP TRIGGER IF EXISTS users_data_insert_trigger ON users;\n'
		)

		stmt_trigger = text(
			(  # noqa: UP032
				'CREATE TRIGGER users_data_insert_trigger\n'
				'AFTER INSERT\n'
				'ON users\n'
				'FOR EACH ROW\n'
				'EXECUTE FUNCTION users_data_insert_function();'
			),
		)

		await session.execute(stmt_func)
		await session.execute(stmt_drop_if_exist)
		await session.execute(stmt_trigger)
		await session.commit()

		return True


	async def engine_create_AppsTesters_on_Dev_delete_trigger(
		self: DBTriggers, session: AsyncSession,
	) -> bool:  # noqa: N802
		# FIXME: Crutch, but ok..
		##
		# TODO: Make compatibility with sqlite..
		stmt4sqlite = text(
			'CREATE TRIGGER apps_tickets_delete_trigger\n'
			'AFTER DELETE\n'
			'ON apps_tickets\n'
			'BEGIN\n'
			'	DELETE FROM apps_testers_data\n'
			'	WHERE ticket_id = OLD.id;\n'
			'END;'
		)

		stmt_func = text(
			'CREATE OR REPLACE FUNCTION apps_tickets_delete_function()\n'
			'RETURNS TRIGGER AS $$\n'
			'BEGIN\n'
			'    DELETE FROM apps_testers_data\n'
			'    WHERE ticket_id = OLD.id;\n'
			'    RETURN OLD;\n'
			'END;\n'
			'$$ LANGUAGE plpgsql;'
		)

		stmt_drop_if_exist = text(
			'DROP TRIGGER IF EXISTS apps_tickets_delete_trigger ON apps_tickets;\n'
		)

		stmt_trigger = text(
			'CREATE TRIGGER apps_tickets_delete_trigger\n'
			'AFTER DELETE\n'
			'ON apps_tickets\n'
			'FOR EACH ROW\n'
			'EXECUTE FUNCTION apps_tickets_delete_function();'
		)

		await session.execute(stmt_func)
		await session.execute(stmt_drop_if_exist)
		await session.execute(stmt_trigger)
		await session.commit()

		return True


	async def engine_create_all(self: DBTriggers, metadata: MetaData = Base.metadata) -> bool:
		##
		ret = await self.db.engine_create_all(metadata)
		async with self.db._session_factory() as session:
			await self.engine_create_UsersData_on_User_insert_trigger(session)
			await self.engine_create_AppsTesters_on_Dev_delete_trigger(session)
			await session.commit()
		return ret
