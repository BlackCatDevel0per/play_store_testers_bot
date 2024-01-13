from __future__ import annotations

from datetime import datetime  # noqa: TCH003
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated  # noqa: UP035

opt_str = Annotated[Optional[str], mapped_column(default=None)]  # noqa: UP007

# TODO: Mb use some models in bot code..
# TODO: repr..


class Base(DeclarativeBase):
	"""Just declarative base class for ORM tables."""

	...

# BigInteger.. Ok..


class UsersTable(Base):
	"""Users (main) table - with default telegram data."""

	__tablename__ = 'users'

	user_id = mapped_column(BigInteger(), primary_key=True)
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
