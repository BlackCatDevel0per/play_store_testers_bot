from aiogram_middlewares.utils import BrotliedPickleSerializer
from loader import dp

from data.config import DB_ENGINE
from data.options.paths import WORKDIR
from utils.misc.logging import logger

from .db import DBMiddleware
from .logging import LoggingMiddleware
from .throttling import RateMiddleware

if __name__ == 'middlewares':
	# ...

	# 5 requests / 10 sec.
	rm = RateMiddleware(## ##1 sec. problems..
		period_sec=10,
		after_handle_count=5,
		warnings_count=3,
		data_serializer=BrotliedPickleSerializer,
		cooldown_message='Охлади своё тр@ханье!',
		calmed_message='П*зда =)',

		# topping_up=False,##
	)


	dp.update.outer_middleware(rm)


	dp.update.middleware(LoggingMiddleware(logger=logger))

	# After filters pass
	dbm = DBMiddleware(engine=DB_ENGINE)

	# FIXME: Crutch..
	if not WORKDIR.joinpath('sqlite3.db').exists():
		import asyncio

		loop = asyncio.get_event_loop()
		loop.run_until_complete(dbm.db.engine_create_all())  # FIXME: Not one of the best ways..

	dp.update.middleware(dbm)
