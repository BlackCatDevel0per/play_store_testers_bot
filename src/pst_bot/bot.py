from __future__ import annotations  # noqa: I001
# import os
# To run on repl.it
# from background import keep_alive

import asyncio
from os import getenv

# WARNING: Import order!!!
import middlewares  # noqa: F401
import filters  # noqa: F401
import handlers  # noqa: F401

# TODO: Use bot arg in middleware & mb delete loader..
from loader import bot, dp

from data.options.paths import WORKDIR
from utils.misc.logging import logger
from utils.notify_admins import on_shutdown_notify, on_startup_notify
from utils.set_bot_commands import set_bot_commands

from middlewares import dbm


# TODO: Move it to another place..
async def check_db() -> None:
	# FIXME: Crutch..
	if not WORKDIR.joinpath('sqlite3.db').exists() or not getenv('DEBUG_MODE'):
		await dbm.db.triggers.engine_create_all()


async def on_startup() -> None:
	await set_bot_commands(bot)

	await check_db()

	await on_startup_notify(bot, logger)


async def on_shutdown():
	await on_shutdown_notify(bot, logger)


async def bot_start() -> None:
	# TODO: Move to other places & use dp.run_polling
	dp.startup.register(on_startup)
	dp.shutdown.register(on_shutdown)
	##
	try:
		await dp.start_polling(
			bot,
			# skip_updates=True,
		)
	finally:
		##
		await bot.session.close()


if __name__ == '__main__':
	# loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(loop)
	# loop.run_until_complete(bot_start())

	# if not os.environ.get('DEBUG_MODE'):
	# 	keep_alive()

	asyncio.run(bot_start())
