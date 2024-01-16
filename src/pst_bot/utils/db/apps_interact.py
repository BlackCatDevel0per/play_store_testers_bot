from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, text, update

from .crud_queries import query__apps_tickets__app_url
from .cruds import DBApp
from .tables import AppsTestersDataTable, AppsTicketsTable, UsersProfileTable, UsersTable

if TYPE_CHECKING:
	from typing import Any, Literal

	from sqlalchemy.ext.asyncio import AsyncSession
	from sqlalchemy.sql.selectable import Select

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Mb `finally` block..
# TODO: Set limits for SELECT queries..


class DBDuplicationError(Exception):
	...


class TicketDuplicationError(DBDuplicationError):
	...


class TesterOfTicketDuplicationError(DBDuplicationError):
	...


class ProfileOptsDuplicationError(DBDuplicationError):
	...


class DBAppsInteract(DBApp):
	"""App for interact with tickets data with apps & etc.."""

	async def _is_ticket_url_exist(
		self: DBAppsInteract,
		session: AsyncSession, app_url: str,
	) -> bool:
		# TODO: Do it other way.. (check using regex..)
		# FIXME: Duplicating..
		query_app_url = query__apps_tickets__app_url\
			.where(AppsTicketsTable.app_url == app_url)\
			.limit(1)
		return bool((await session.execute(query_app_url)).scalar_one_or_none())


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

		except TicketDuplicationError:
			raise

		except Exception:
			logger.exception('Ticket ADD with data `%s` failed!', new_ticket)
			return False

		else:
			return True


	async def _is_user_profile_exist(
		self: DBAppsInteract,
		session: AsyncSession, user_id: int,
	) -> bool:
		# TODO: Do it other way.. (check using regex..)
		# FIXME: Duplicating..
		# FIXME: 'query' at end or begin??
		query_profile_by_user_id = select(UsersProfileTable)\
			.where(UsersProfileTable.user_id == user_id)\
			.limit(1)
		return bool((await session.execute(query_profile_by_user_id)).scalar_one_or_none())


	# TODO: Upserting..?
	# TODO: Use kw by default..
	async def add_profile_options(
		self: DBAppsInteract,
		user_id: int,
		gmails: str,
	) -> bool:
		# FIXME: Duplicating..
		try:
			new_profile = UsersProfileTable(
				user_id=user_id,
				gmails=gmails,
			)

			async with self.db._session_factory() as session:
				if await self._is_user_profile_exist(session, user_id):
					raise ProfileOptsDuplicationError

				session.add(new_profile)

				await session.flush()
				await session.commit()

				await session.refresh(new_profile)

				logger.info(
					'New Profile opts id#%i of user_id`%i`, gmails `%s` ADDED',
					new_profile.id, user_id, gmails,
				)

		except ProfileOptsDuplicationError:
			raise

		except Exception:
			logger.exception('New Profile ADD with data `%s` failed!', new_profile)
			return False

		else:
			return True


	async def update_profile_options(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
		update_cols: dict[str, Any],  # data
	) -> bool:
		# FIXME: Duplicating..
		try:
			async with self.db._session_factory() as session:

				profile_update_query = update(UsersProfileTable)\
					.filter_by(**search_properties)\
					.values(update_cols)

				await session.execute(profile_update_query)

				# FIXME: Use autocommit & mb autoflush in context manager..
				await session.flush()
				await session.commit()


				logger.info(
					'Profile by params `%s`, "%s" UPDATED',
					search_properties, update_cols,
				)

		except Exception:
			# FIXME: Log params.. & by or with 'params'??
			logger.exception('Profile UPDATE with data `%s` failed!', update_cols)
			return False

		else:
			return True


	# FIXME: Make private..
	async def get_profile_options_of(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> UsersProfileTable:
		try:
			async with self.db._session_factory() as session:

				# FIXME: 'sel' naming..
				profile_sel_query = select(UsersProfileTable).filter_by(**search_properties).limit(1)

				ret = await session.execute(profile_sel_query)
				profile = ret.scalar_one()

				##
				#
				logger.info(
					'Profile opts with id#%i of user_id#%i GOT..',
					profile.id, profile.user_id,
				)

				return profile

		except Exception:
			# FIXME: Properly repr some models data..
			logger.exception('Profile opts GOT with data `%s` failed!', search_properties)
			raise


	# FIXME: Move into the other package..
	def query_find_tickets_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> Select:
		# TODO: Give the way to use tuple with ORM query conditions/parts..
		return select(AppsTicketsTable).filter_by(**search_properties)


	# FIXME: Make private..
	async def get_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> AppsTicketsTable:
		try:
			async with self.db._session_factory() as session:

				ticket_query = self.query_find_tickets_by(search_properties).limit(1)

				ret = await session.execute(ticket_query)
				ticket = ret.scalar_one()

				logger.info(
					'Ticket id#%i `%s` added by dev `%i`/`%s` GOT..',
					ticket.id, ticket.app_name, ticket.by_dev_id, ticket.by_dev_username,
				)

				return ticket

		except Exception:
			# FIXME: Properly repr some models data..
			logger.exception('Ticket GOT with data `%s` failed!', search_properties)
			raise


	async def _is_tester_joined_to_ticket(
		self: DBAppsInteract,
		session: AsyncSession,
		*,
		tester_id: int, ticket_id: int,
	) -> bool:
		testers_sel_query = select(AppsTestersDataTable)\
			.where(
				AppsTestersDataTable.tester_id == tester_id,
				AppsTestersDataTable.ticket_id == ticket_id,
		)
		#

		return bool((await session.execute(testers_sel_query)).scalar_one_or_none())


	# TODO: Group some methods to child classes..
	async def join_tester_to_ticket(
		self: DBAppsInteract,
		*,
		tester_id: int, ticket_id: int,
	) -> bool:
		try:
			new_tester = AppsTestersDataTable(
				tester_id=tester_id,
				ticket_id=ticket_id,
			)

			async with self.db._session_factory() as session:
				if await self._is_tester_joined_to_ticket(
					session, tester_id=tester_id, ticket_id=ticket_id,
				):
					raise TesterOfTicketDuplicationError

				session.add(new_tester)

				await session.flush()
				await session.commit()

				await session.refresh(new_tester)

				logger.info(
					'New Tester id#%i associated with Ticket id`%i` ADDED',
					tester_id, ticket_id,
				)

		except Exception:
			logger.exception(
				'New Tester ADD id#%i associating with Ticket id`%i` Failed!',
				tester_id, ticket_id,
			)
			return False

		# TODO: Do it with all..
		else:
			return True


	async def get_testers_of_ticket(
		self: DBAppsInteract,
		ticket_id: int,
	) -> list[AppsTestersDataTable]:
		# TODO: Set limits..?
		try:
			async with self.db._session_factory() as session:

				ticket_testers_query = select(UsersTable)\
					.join(
						AppsTestersDataTable,
						AppsTestersDataTable.tester_id == UsersTable.user_id,
					)\
					.where(AppsTestersDataTable.ticket_id == ticket_id)

				ret = await session.execute(ticket_testers_query)
				# TODO: raise if no data..?
				# TODO: Recheck if I used fetchall in some places..
				testers = ret.scalars().all()

				logger.info(
					'GOT.. testers (%i) of ticket id`%i`',
					len(testers), ticket_id,  ##
				)

				return testers

		except Exception:
			logger.exception('Ticket GOT testers by id`%i` failed!', ticket_id)
			raise


	async def get_tickets_of(
		self: DBAppsInteract,
		search_properties: dict[str, Any],  # Only user_id or username
	) -> list[AppsTicketsTable]:
		# NOTE: Use one param or multiple..? (if two exists)
		if not (
			AppsTicketsTable.by_dev_id.name in search_properties
			or
			AppsTicketsTable.by_dev_username.name in search_properties
		):
			msg = 'Only telegram user_id or username are allowed!'
			raise ValueError(msg)

		try:
			async with self.db._session_factory() as session:

				ticket_query = self.query_find_tickets_by(search_properties)

				ret = await session.execute(ticket_query)
				# TODO: raise if no data..?
				tickets = ret.scalars().all()

				logger.info(
					'GOT.. tickets count `%i` by params `%s`',
					len(tickets), search_properties,  ##
				)

				return tickets

		except Exception:
			logger.exception('Ticket GOT by params `%s` failed!', search_properties)
			raise


	async def update_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
		update_cols: dict[str, Any],
	) -> bool:
		try:
			async with self.db._session_factory() as session:

				ticket_update_query = update(AppsTicketsTable)\
					.filter_by(**search_properties)\
					.values(update_cols)

				await session.execute(ticket_update_query)

				await session.flush()
				await session.commit()


				logger.info(
					'Ticket by params `%s`, "%s" UPDATED',
					search_properties, update_cols,
				)

				return True

		except Exception:
			# FIXME: Log params.. & by or with 'params'??
			logger.exception('Ticket UPDATE with data `%s` failed!', update_cols)
			return False


	async def del_ticket_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
	) -> bool:
		try:
			async with self.db._session_factory() as session:

				# TODO: Move into the one package..
				ticket_delete_query = delete(AppsTicketsTable).filter_by(**search_properties)

				await session.execute(ticket_delete_query)
				await session.commit()

				logger.info(
					'Ticket by params `%s` DELETED',
					search_properties,
				)

				return True

		except Exception:
			logger.exception('Ticket DELETE by params `%s` failed!', search_properties)
			return False


	async def testers_counter_action_by(
		self: DBAppsInteract,
		search_properties: dict[str, Any],
		action: Literal['+', '-'], num: int,
		##
		counter: Literal['active_testers_count', 'pending_testers_count'] = 'active_testers_count',
	) -> bool:
		# Check counter col & action..
		if len(action) != 1 and action not in ('+', '-') or \
			counter not in ('active_testers_count', 'pending_testers_count'):
			raise ValueError

		try:
			async with self.db._session_factory() as session:

				cc = getattr(AppsTicketsTable, counter)
				tc_update_query_val_p = cc + num
				tc_update_query_val_m = cc - num
				tc_update_query = update(AppsTicketsTable)

				gen_tc_query = lambda val: tc_update_query\
					.values(
						{
							AppsTicketsTable.active_testers_count.name: val,
						},
					).filter_by(**search_properties)

				if action == '+':
					ticket_count_query = gen_tc_query(tc_update_query_val_p)
				else:
					ticket_count_query = gen_tc_query(tc_update_query_val_m)

				# get_count_query = text(
				# 	f'SELECT {counter}'  # noqa: S608
				# 	' '
				# 	'FROM :table WHERE id = :ticket_id'
				# )

				await session.execute(ticket_count_query)

				await session.flush()
				await session.commit()

				# FIXME: Make pattern for such logs..
				logger.info(
					'Ticket COUNTER UPDATED to `%s%i`, by params `%s`',
					action, num, search_properties,
				)

				return True

		except Exception:
			logger.exception(
				'Ticket COUNTER UPDATE to `%s%i`, with params `%s` failed!',
				action, num,
				search_properties,
			)
			return False


	## TODO: Update ticket data (with skip & cancelling from bot side),
	# TODO: list tickets with options~,
	# TODO: list gmails of testers~ using profile(s) table data..
	# TODO: profile..

	# TODO: Some amount of methods for exporting data for archive..

	# TODO: Archive/backup/export old tickets with testers info..

	# TODO: In-busy counters.. (gmails, _max_apps_)

	# TODO: Methods from bot side..

	# TODO: Marks for system reqs with OS, RAM & etc.

	# TODO: ! Update statuses methods !

	# TODO: From bot side (again) timer for delete/cancel tester approve/join request
