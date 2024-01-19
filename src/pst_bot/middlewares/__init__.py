import os

from aiogram_middlewares.utils import BrotliedPickleSerializer

from data.config import DB_ENGINE
from data.options.paths import WORKDIR
from loader import dp
from utils.misc.logging import logger

from .db import DBMiddleware
from .logging import LoggingMiddleware
from .throttling import RateMiddleware

if __name__ == 'middlewares':
	# ...

	# 5 requests / 10 sec.
	rm = RateMiddleware(## ##1 sec. problems..
		period_sec=15,
		after_handle_count=8,
		warnings_count=3,
		data_serializer=BrotliedPickleSerializer,
		cooldown_message='Не спамь!',
		calmed_message='Можете писать =)',

		# topping_up=False,##
	)


	dp.update.outer_middleware(rm)


	dp.update.middleware(LoggingMiddleware(logger=logger))

	# After filters pass
	dbm = DBMiddleware(engine=DB_ENGINE)

	# FIXME: Crutch..
	if not WORKDIR.joinpath('sqlite3.db').exists() or not os.environ.get('DEBUG_MODE'):
		import asyncio

		loop = asyncio.get_event_loop()
		# FIXME:
		loop.run_until_complete(dbm.db.triggers.engine_create_all())  # FIXME: Not one of the best ways..

	dp.update.middleware(dbm)
