import logging
import os
from datetime import datetime

from rich.logging import RichHandler

from data.options import LOGGING_LEVEL

handlers = [RichHandler(markup=True, rich_tracebacks=True)]

if os.environ.get('DEBUG_MODE'):
	fh = logging.FileHandler(
	    filename=(
			'bot_log-'
			f"{datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S')}"
	        '.log'
		),
	)
	fh.setLevel(logging.DEBUG)

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
