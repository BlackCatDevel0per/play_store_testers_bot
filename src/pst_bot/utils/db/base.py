from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from tg_users import DBChannelsSubscriptions, DBTGBase

from .apps_interact import DBAppsInteract
from .cruds import ComfortCRUD
from .triggers import DBTriggers

if TYPE_CHECKING:
	from typing import Any

logger = logging.getLogger('bot')  # FIXME: Rename to ORM or DB or etc. & Manage loggers!!!

# TODO: Mb `finally` block..


class DB(ComfortCRUD):
	def __init__(self: DB, *args: Any, **kwargs: Any) -> None:
		super().__init__(*args, **kwargs)

		self.tg_users = DBTGBase(self)
		self.tg_chns_sub = DBChannelsSubscriptions(self)
		self.triggers = DBTriggers(self)

		self.apps = DBAppsInteract(self)
