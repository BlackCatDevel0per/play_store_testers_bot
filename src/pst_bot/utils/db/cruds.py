from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, func, insert, select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

if TYPE_CHECKING:
	# Can use dict & Mapping =)
	from collections.abc import Iterable, Mapping, Sequence
	from typing import Any

	from sqlalchemy import MetaData, Table
	from sqlalchemy.engine.cursor import LegacyCursorResult
	from sqlalchemy.ext.asyncio import AsyncSession
	from sqlalchemy.sql.selectable import Select

	from .base import DB


class DBApp:
	"""Just helper class for main DB apps.

	XD
	"""

	def __init__(self: DBApp, parent_base_ins: DB) -> None:
		self.db = parent_base_ins


class ComfortCRUD:
	def __init__(self: ComfortCRUD, engine: str, pool_size=5, max_overflow=10) -> None:
		engine_db_type = engine.split('+', maxsplit=1)[0]
		# Crutch..
		if engine_db_type != 'sqlite':
			self._engine = create_async_engine(engine, pool_size=pool_size, max_overflow=max_overflow)
			# TODO: Warning..
		else:
			self._engine = create_async_engine(
				engine,
				# echo=True,
			)
		self._session_factory: AsyncSession = async_sessionmaker(self._engine)


	async def engine_create_all(self: ComfortCRUD, metadata: MetaData) -> bool:
		###
		async with self._engine.connect() as conn:
			await conn.run_sync(metadata.create_all)
		return True


	# async def select_one(self: ComfortCRUD, column: Column, from_table: Table, where: list[Column] | None) -> any:
	# 	# Does ORM has thing like this? Hmm..
	# 	sel = select(column).select_from(from_table)
	# 	fetch = await self.conn.execute(sel)
	# 	return fetch.fetchone()[0]


	# FIXME: Remove or do something with it..
	async def _session_execute_fetch_one_or_none(self: ComfortCRUD, session: AsyncSession, select: Select) -> Any:
		# Does ORM has thing like this? Hmm..
		return (await session.execute(select)).scalar_one_or_none()  # FIXME: Return sentinel..


	async def select_cols_from(##
		self: ComfortCRUD,
		session: AsyncSession,
		table_or_cols: Table | list[Column],
		where: list[Column] | None = None,
		*,
		FetchOne: bool = False,
	) -> list[tuple] | list:
		# s = select(table_or_cols)
		if not isinstance(table_or_cols, Column):  # mb sequence
			table_or_cols = table_or_cols[0]
		s = select(table_or_cols)
		if where:##
			s = s.where(*where)
		r = await session.execute(s)
		res: list[tuple] | list  # Empty list if no records
		# print(s.compile().params)
		res = r.fetchall() if not FetchOne else r.fetchone()
		return res if isinstance(res, list) else [res]


	def rows2dicts(
		self: ComfortCRUD,
		keys: list[Column.header], rows: Iterable[Sequence],
	) -> Iterable[dict]:  # seq..
		for row in rows:
			yield dict(tuple(zip(keys, row)))


	# FIXME: lru..
	def get_columns(self: ComfortCRUD, table: Table) -> list[Column]:
		return [column.key for column in table.c]


	async def get_from_table(self: ComfortCRUD, table: Table, *, FetchOne: bool = False) -> list[dict]:
		async with self._session_factory() as session:
			data = await self.select_cols_from(session, table, FetchOne=FetchOne)
			# Fetch to dict (json)
			columns = self.get_columns(table)
			return list(self.rows2dicts(columns, data))


	# Need more typization.. (in other projects too)
	# & commits!!!
	async def insert_into(
		self: ComfortCRUD, session: AsyncSession, table: Table, data: list[dict],
	) -> LegacyCursorResult:  # need see results like rows_count, primary_keys_count & etc.
		ins = insert(table)##
		# print(ins.values(data[0]), data[0].values())
		return await session.execute(ins, data)


	# mb need apply that for other projects =)
	# ??
	async def insert_ine_by_key(
		self: ComfortCRUD, table: Table, data: list[Any] | list[Mapping], data_key: str | Column | None = None,
	) -> bool | None:
		async with self._session_factory() as session:
			"""One of the best choices for db-loaded rows))."""
			data_key = data_key if data_key is not None else self.get_columns(table)[0]
			data_key_col: Column = getattr(table.c, data_key)
			wasted: int = 0  # Count
			data_len: int = len(data)  # Length
			# key_cols: 'Union[UniRowType_in_List, List]' = [row[0] for row in self.select_cols_from(session, [data_key_col])]
			key_cols: list[Any] | list = [row[0] for row in await self.select_cols_from(session, data_key_col)]  # `Any` is db row type
			#
			while data_len > 0 and wasted < data_len:
				# list with mappings (List[Mapping] or Mappings)
				# dr in cycle is `UniAdsRowDB`
				# dv in cycle is `UniAdsRowType`
				for i, dr in enumerate(data):
					dv = dr[data_key]
					if dv in key_cols:
						del data[i]
						# print('del', data.pop(i))
						data_len -= 1
					else:
						wasted += 1
			del key_cols
			# if exception need to return with raise..
			if data:
				await self.insert_into(session, table, data)
				return True
			return None  ##


	# You can use truncate(_all)..
	async def truncate_table(self: ComfortCRUD, table: Table) -> bool:
		# FIXME: ...
		async with self._session_factory() as session:
			await session.execute(text("TRUNCATE TABLE :table").bindparams(table=table))##
			return True
