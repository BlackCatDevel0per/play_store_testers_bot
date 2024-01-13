from __future__ import annotations  # noqa: I001

import asyncio

# WARNING: Import order!!!
import middlewares  # noqa: F401
import filters  # noqa: F401
import handlers  # noqa: F401

# TODO: Use bot arg in middleware & mb delete loader..
from loader import bot, dp

from utils.misc.logging import logger
from utils.notify_admins import on_shutdown_notify, on_startup_notify
from utils.set_bot_commands import set_bot_commands


async def on_startup() -> None:
	await set_bot_commands(bot)

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

	asyncio.run(bot_start())
