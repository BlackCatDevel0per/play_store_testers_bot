from __future__ import annotations

from datetime import datetime  # noqa: TCH003
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated  # noqa: UP035

opt_str = Annotated[Optional[str], mapped_column(default=None)]  # noqa: UP007

ticket_field = Annotated[str, mapped_column(String(128))]
ticket_big_field = Annotated[str, mapped_column(String(512))]

# TODO: Mb use some models in bot code..
# TODO: repr..


class Base(DeclarativeBase):
	"""Just declarative base class for ORM tables."""

	...

# BigInteger.. Ok..


class UsersTable(Base):
	"""Users (main) table - with default telegram data."""

	__tablename__ = 'users'

	user_id = mapped_column(BigInteger(), unique=True, primary_key=True)
	username: Mapped[Optional[str]] = mapped_column(String(32), default=None)  # min 5  # noqa: UP007
	full_name: Mapped[opt_str] = mapped_column(String(132), default=None)
	language_code: Mapped[opt_str] = mapped_column(String(3))
	datetime: Mapped[Optional[datetime]] = mapped_column(default=None, server_default=func.current_timestamp())  # noqa: UP007


class UsersDataTable(Base):
	"""Users data table - with data for interacting users with models."""

	__tablename__ = 'users_data'

	user_id = mapped_column(BigInteger(), ForeignKey(UsersTable.user_id, ), primary_key=True)  # TODO: Mb on user delete trigger in DB class..
	current_language_code: Mapped[str] = mapped_column(default='ru')


class UsersChannelsSubscriptionsTable(Base):
	"""Users channels subscriptions data table - with data for interacting users channels.."""

	__tablename__ = 'users_channels_subscriptions'

	id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

	user_id = mapped_column(BigInteger(), ForeignKey(UsersTable.user_id, ))  # TODO: Mb on user delete trigger in DB class..
	channel_id = mapped_column(BigInteger(), nullable=False)


# TODO: Profiles table with ~options (aka options table)..
class UsersProfileTable(Base):

	__tablename__ = 'users_profile'

	id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

	user_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)

	# TODO: Move into the other table..
	# Lazy move..
	gmails: Mapped[str] = mapped_column(String(), nullable=False)  # gmails comma separated..


# TODO: From users-side optionally hide some opts..
class AppsTicketsTable(Base):
	"""Devs apps tickets data (made by devs, view by users)."""

	__tablename__ = 'apps_tickets'

	id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003


	# Owner data
	# FIXME: Foreign keys in pg -_-
	by_dev_id = mapped_column(BigInteger(), nullable=False)#, ForeignKey(UsersTable.user_id, ))  # TODO: Mb on user delete trigger in DB class..
	by_dev_username = mapped_column(String(32), default=None)#, ForeignKey(UsersTable.username, ))

	active_testers_count: Mapped[int] = mapped_column(default=0)

	# TODO
	pending_testers_count: Mapped[int] = mapped_column(default=0)

	app_name: Mapped[ticket_field] = mapped_column(nullable=False)
	description: Mapped[ticket_big_field]
	app_url: Mapped[str] = mapped_column(String(256), nullable=False)

	# ~approximately
	dev_response_period = mapped_column(String(32), default='-')  # TODO: Table with schedules..

	# __table_args__ = (
	# 	ForeignKeyConstraint(
	# 		[by_dev_id, by_dev_username],
	# 		[UsersTable.user_id, UsersTable.username],
	# 	),
	# )


class AppsTestersDataTable(Base):
	"""Tickets data related with users (devs & testers - made by testers, view by devs)."""

	__tablename__ = 'apps_testers_data'

	id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

	ticket_id: Mapped[int] = mapped_column(nullable=False)

	# TODO: Sent tg message id.. & mb check if message removed from bot side & resend..

	tester_id = mapped_column(BigInteger(), ForeignKey(UsersTable.user_id, ), nullable=False)  # TODO: Mb on user delete trigger in DB class..

	# TODO: Use bools..
	dev_status: Mapped[str] = mapped_column(String(16), default='accepted', nullable=False)
	tester_status: Mapped[str] = mapped_column(String(16), default='wait', nullable=False)
