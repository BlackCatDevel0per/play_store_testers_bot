from aiogram.fsm.state import State, StatesGroup


class FSMMsgsListen2Gen(StatesGroup):
	"""For listen user's message text & generate tts that OwO."""

	listen = State()
