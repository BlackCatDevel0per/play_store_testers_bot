from __future__ import annotations

import json
import os

# TODO: Configparser and load from `.env`
# TODO: Better names for these env vars..

BOT_TOKEN = os.environ['BOT_TOKEN']
ADMINS: tuple[int, ...] = tuple(json.loads(os.environ['ADMINS']))

# WARNING: Channel ids subscribe to & with some upper perms too..
CHANNELS_IDS = (
	-1234567891011,
)

CHANNELS_LINKS = {
	'Some channel 🌚': 'https://t.me/...',
}


# PostgreSQL Derver for future =)
# DB_ENGINE = os.environ['DB_ENGINE']
DB_ENGINE = 'sqlite+aiosqlite:///sqlite3.db'
