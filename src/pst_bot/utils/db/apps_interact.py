from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import select, text

from .crud_queries import query__apps_tickets__app_url
from .cruds import DBApp
from .tables import AppsTicketsTable

if TYPE_CHECKING:
	from typing import Any, Literal

	from sqlalchemy.ext.asyncio import AsyncSession
	from sqlalchemy.sql.selectable import Select

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Mb `finally` block..


class TicketDuplicationError(Exception):
	...


class DBAppsInteract(DBApp):
	"""App for interact with tickets data with apps & etc.."""

	async def _is_ticket_url_exist(
		self: DBAppsInteract,
		session: AsyncSession, app_url: str,
	) -> bool:
		# TODO: Do it other way.. (check using regex..)
		# FIXME: Duplicating..
		# FIXME: Remove stupid things..
		query_app_url = query__apps_tickets__app_url.where(AppsTicketsTable.app_url == app_url)
		fetch: int | None = await self.db._session_execute_fetch_one_or_none(session, query_app_url)
		del query_app_url
		##
		if fetch:
			del fetch
			return True
		del fetch
		return False


	async def add_ticket(
		self: DBAppsInteract,
		by_dev_id: int,
		by_dev_username: str,

		app_name: str,
		description: str,
		app_url: str,

		dev_response_period: str = '-',
	) -> bool:
		try:
			new_ticket = AppsTicketsTable(
				by_dev_id=by_dev_id,
				by_dev_username=by_dev_username,

				app_name=app_name,
				description=description,
				app_url=app_url,

				dev_response_period=dev_response_period,
			)

			async with self.db._session_factory() as session:
				if await self._is_ticket_url_exist(session, app_url):
					msg = 'Looks like %s already exists in db..'
					raise TicketDuplicationError(msg % app_url)

				session.add(new_ticket)

				await session.flush()
				await session.commit()

				await session.refresh(new_ticket)

				logger.info(
					'New Ticket id#%i `%s` added by dev `%i`/`%s` ADDED',
					new_ticket.id, app_name, by_dev_id, by_dev_username,
				)

				return True

		except TicketDuplicationError:
			raise

		except Exception:
			logger.exception('Ticket add with data `%s` failed!', new_ticket)
			return False


	def sess_find_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> Select:
		"""Find and return ticket using column names as keys & values as data (doesn't fetch!).

		```python
		async with db._session_factory() as session:
			ticket = await db.apps.sess_find_ticket_by(session).first()
			print(ticket)
		```
		"""
		# TODO: Give the way to use tuple with ORM query conditions/parts..
		return select(AppsTicketsTable)\
		.filter_by(**search_properties)


	async def get_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> AppsTicketsTable:
		try:
			async with self.db._session_factory() as session:

				ticket_query = self.sess_find_ticket_by(search_properties)

				ret = await session.execute(ticket_query)
				ticket = ret.fetchone()[0]

				logger.info(
					'Ticket id#%i `%s` added by dev `%i`/`%s` GOT..',
					ticket.id, ticket.app_name, ticket.by_dev_id, ticket.by_dev_username,
				)

				return ticket

		except Exception:
			logger.exception('Ticket GOT with data `%s` failed!', ticket)
			raise


	async def update_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
		update_cols: dict[str, Any],
	) -> bool:
		try:
			async with self.db._session_factory() as session:

				ticket = self.sess_find_ticket_by(search_properties).first()

				for column, value in update_cols.items():
					setattr(ticket, column, value)

				await session.flush()
				await session.commit()

				logger.info(
					'Ticket id#%i `%s` added by dev `%i`/`%s` UPDATED',
					ticket.id, ticket.app_name, ticket.by_dev_id, ticket.by_dev_username,
				)

				return True

		except Exception:
			logger.exception('Ticket UPDATE with data `%s` failed!', ticket)
			return False


	async def del_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> bool:
		try:
			async with self.db._session_factory() as session:

				ticket = self.sess_find_ticket_by(search_properties)

				ticket.delete()

				await session.flush()
				await session.commit()

				logger.info(
					'Ticket id#%i `%s` added by dev `%i`/`%s` DELETED',
					ticket.id, ticket.app_name, ticket.by_dev_id, ticket.by_dev_username,
				)

				return True

		except Exception:
			logger.exception('Ticket DELETE with data `%s` failed!', ticket)
			return False


	async def testers_counter_action(
		self: DBAppsInteract,
		ticket_id: int,
		action: Literal['+', '-'], num: int,
		counter: Literal['active_testers_count', 'pending_testers_count'] = 'active_testers_count',
	) -> bool:
		if action not in ('+', '-') or counter in ('active_testers_count', 'pending_testers_count'):
			raise ValueError

		if not isinstance(ticket_id, int):
			raise TypeError

		try:
			async with self.db._session_factory() as session:

				query = text(
					'UPDATE tickets SET :counter = :counter'
					' '
					':action :count_up'
					' '
					'WHERE id = :ticket_id RETURNING :counter'
				)

				ret = await session.execute(
					query,
					{
						'ticket_id': ticket_id, 'count_up': num,
						'action': action, 'counter': counter,
					},
				)
				count = ret.fetchone()[0]  ##

				# FIXME: Make pattern for such logs..
				logger.info(
					'Ticket id#%i COUNTER UPDATED to %i, now `%i`',
					ticket_id, num, count,
				)

				return True

		except Exception:
			logger.exception('Ticket COUNTER UPDATE with ticket_id `%s` failed!', ticket_id)
			return False


	## TODO: Update ticket data (with skip & cancelling from bot side),
	# TODO: count active app testers by ticket_id, list tickets with options,
	# TODO: list gmails of testers using profile(s) table data..
	# TODO: get profile data & profile..

	# TODO: Some amount of methods for exporting data for archive..

	# TODO: Archive/backup/export old tickets with testers info..

	# TODO: In-busy counters.. (gmails, _max_apps_)

	# TODO: Methods from bot side..

	# TODO: Marks for system reqs with OS, RAM & etc.

	# TODO: ! Update statuses methods !

	# TODO: From bot side (again) timer for delete/cancel tester approve/join request
