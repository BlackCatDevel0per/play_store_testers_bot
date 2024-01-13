from aiogram.fsm.state import State, StatesGroup


class FSMAdminsMessagingAccept(StatesGroup):
	"""For admins spamming command."""

	message = State()
	accept_and_continue = State()
