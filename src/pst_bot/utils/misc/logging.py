import logging
from datetime import datetime, timezone
from pathlib import Path

from rich.logging import RichHandler

from data.options import LOGGING_LEVEL

handlers = [RichHandler(markup=True, rich_tracebacks=True)]

#
logs_dir = Path('logs')
logs_dir.mkdir(parents=True, exist_ok=True)

current_logfile = logs_dir.joinpath(  # TODO: Refactor..
	'bot_log-'
	f"{datetime.strftime(datetime.now(tz=timezone.utc), '%Y-%m-%d_%H%M%S')}"
	'.log'
)

fh = logging.FileHandler(current_logfile)
fh.setLevel(logging.DEBUG)

handlers.append(fh)

logging.basicConfig(
	format='%(message)s',
	level=logging.INFO,
	# force=True,  # Use just for see other logging handlers

	handlers=handlers,
)

DEFAULT_LOGGER = 'bot'

logger = logging.getLogger(DEFAULT_LOGGER)

logger.setLevel(LOGGING_LEVEL)
# TODO: Hide bot info in logs..
logging.getLogger('aiogram_middlewares').setLevel(logging.INFO)
# logging.getLogger('aiogram_middlewares').setLevel(LOGGING_LEVEL)

logging.info('%s', f'{LOGGING_LEVEL=}')
