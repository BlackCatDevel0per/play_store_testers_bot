from aiogram_middlewares.utils import BrotliedPickleSerializer

from data.config import DB_ENGINE
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

	dp.update.middleware(dbm)
