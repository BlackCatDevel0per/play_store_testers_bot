from aiogram import F

# TODO: Move more filters..

# Legends.. UwU
_endswith = ('?', '!', '.')  # lol, in docs set XD
_MIN_MESSAGE_LENGTH = 5
_MAX_MESSAGE_LENGTH = 200  # 10
# Commands
# TODO: Speed check..
filter_message_not_empty_command_args4gen = F.args.strip()  # FIXME: Rename..
filter_message_empty_command_args4gen = ~filter_message_not_empty_command_args4gen

_message_not_empty_command_args4gen_length = filter_message_not_empty_command_args4gen.len()
filter_message_invalid_command_args4gen = (  # 4help
	filter_message_empty_command_args4gen
	|
	_message_not_empty_command_args4gen_length.func(lambda nea: nea < _MIN_MESSAGE_LENGTH or nea > _MAX_MESSAGE_LENGTH)
)  # Hmm..


# Inline
# TODO: Speed check..
# TODO: Mb QueryUse filter like CommandUse..
filter_inline_not_empty_query_data = F.query.strip()
filter_inline_empty_query_data = ~filter_inline_not_empty_query_data

_inline_not_empty_query_data_length = filter_inline_not_empty_query_data.len()
filter_inline_valid_query_data4gen = (
	# Empty data handled by other handler
	_inline_not_empty_query_data_length.func(lambda neq: _MAX_MESSAGE_LENGTH > neq > _MIN_MESSAGE_LENGTH)
	&
	filter_inline_not_empty_query_data.endswith(_endswith)  # TODO: Remove or change to regex..
)
