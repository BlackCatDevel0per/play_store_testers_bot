from aiogram.fsm.state import State, StatesGroup


# NOTE: Does bandit checks code cases like snake_case?
# NOTE: Whi not use as enum & what has `State` class..?
class FSMNewTicket(StatesGroup):
	"""New ticket dialog."""

	set_app_name = State()
	set_description = State()
	set_app_url = State()

	confirm = State()
