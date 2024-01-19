from __future__ import annotations

from dataclasses import replace as replace_fields
from typing import TYPE_CHECKING

from aiogram import F
from aiogram.filters import Command, Filter
from aiogram.filters.command import CommandException, CommandPatternType, Pattern
from aiogram.types import Message

from data.config import CHANNELS_IDS
from keyboards.inline import keyboard_channels_links_list

if TYPE_CHECKING:
	from collections.abc import Sequence
	from typing import Any

	from aiogram import Bot, CommandObject
	from magic_filter import MagicFilter

	from utils.db import DB


# TODO: Move to different lib..
# TODO: Type hints..
class CommandTrigger(Command):
	# lol, `__slots__`..
	"""Custom `Command` filter class variant with minor fixes.."""

	def __init__(self: CommandTrigger, *args, **kwargs) -> None:
		# TODO: Make the same for mentions, do_magic..
		# TODO: Add `strip_args` option..
		# TODO: Make simple repr&str..
		# This works faster than checking at each iteration of the cycle of parent method `validate_command`
		# TODO: Type hint..

		super().__init__(*args, **kwargs)
		if kwargs.get('ignore_case'):
			self._validate_command_case = self._validate_command_ignore_case  # type: ignore

	@staticmethod
	def _validate_command_case(command: CommandObject) -> str:
		return command.command

	def _validate_command_ignore_case(self: CommandTrigger, command: CommandObject) -> str:
		return CommandTrigger._validate_command_case(command).casefold()

	# validate_commands..
	def validate_command(self: CommandTrigger, command: CommandObject) -> CommandObject:
		# Why in `Command.validate_command` `cast`?? You could use it in `__init__` or like this:
		self.commands: tuple[CommandPatternType]
		for allowed_command in self.commands:
			# Command can be presented as regexp pattern or raw string
			# then need to validate that in different ways
			# TODO: Move this regexp stuff to the other method..
			if isinstance(allowed_command, Pattern):  # Regexp
				result = allowed_command.match(command.command)
				if result:
					return replace_fields(command, regexp_match=result)

			command_name = self._validate_command_case(command)
			if command_name == allowed_command:  # String
				return command
		# TODO: Use santitel instead of this exception..
		raise CommandException("Command did not match pattern")

	def validate_prefix(self: CommandTrigger, command: CommandObject) -> None:
		# Not `if command.prefix not in self.prefix:`!!!
		if command.prefix != self.prefix:
			msg = "Invalid command prefix"
			raise CommandException(msg)


filter_no_args = ~F.args.strip()


class CommandUse(CommandTrigger):
	"""Custom `CommandTrigger``Command` filter class with usage reply."""

	def __init__(
		self: CommandUse,
		*values: CommandPatternType,
		commands: Sequence[CommandPatternType] | CommandPatternType | None = None,
		prefix: str = '/',
		ignore_case: bool = False,
		ignore_mention: bool = False,
		magic: MagicFilter | None = None,
		magic4usage: MagicFilter | None = filter_no_args,  # noqa: B008
		usage_text: str = '...',
		usage_text_template: str = 'Usage: {prefix}{{command}} args\nYour args: {{command_args}}\n{usage_text}',
	):
		# TODO: Usage text with template..
		# TODO: Handle exceptions..
		super().__init__(
			*values,
			commands=commands,
			prefix=prefix,
			ignore_case=ignore_case,
			ignore_mention=ignore_mention,
			magic=magic,
		)
		self.usage_text = usage_text
		# TODO: Add more text formats..
		self.usage_text_template = usage_text_template.format(
			usage_text=usage_text, prefix=self.prefix,
		)
		if magic4usage:
			# `self.__call` won't be used
			self.__call = super().__call__  # type: ignore
		self.magic4usage = magic4usage

	def __str__(self: CommandUse) -> str:
		return self._signature_to_string(
			*self.commands,
			prefix=self.prefix,
			ignore_case=self.ignore_case,
			ignore_mention=self.ignore_mention,
			magic=self.magic,
			magic4usage=self.magic4usage,
			usage_text=self.usage_text,
			usage_text_template=self.usage_text_template,
		)

	async def reply_usage(self: CommandUse, bot: Bot, message: Message, command: CommandObject) -> None:
		# TODO: Exceptions handle..
		# TODO: Optional func what should to after..?
		await bot.send_message(message.chat.id, self.usage_text_template.format(command=command.command, command_args=command.args or ''))

	def do_magic4result(self: CommandUse, command: CommandObject) -> Any:
		"""Call only for command usage on `magic4usage` arg condition pass! (in `__init__`)."""
		return self.magic4usage.resolve(command)


	async def __call__(self: CommandUse, message: Message, bot: Bot) -> bool | dict[str, Any]:
		return await CommandUse.__call(self, message, bot)

	@staticmethod##
	async def __call(self: CommandUse, message: Message, bot: Bot) -> bool | dict[str, Any]:
		if not isinstance(message, Message):
			return False

		text = message.text or message.caption
		if not text:
			return False

		try:
			command = await self.parse_command(text=text, bot=bot)
			if self.do_magic4result(command):
				await self.reply_usage(bot, message, command)
				return False
		except CommandException:
			return False
		result = {"command": command}
		if command.magic_result and isinstance(command.magic_result, dict):
			result.update(command.magic_result)
		return result


# TODO: Add 10 min ttl..
class UserSubscribed(Filter):
	async def __call__(self: UserSubscribed, message: Message, bot: Bot, db: DB) -> bool:
		is_subscribed = await db.is_user_subscribed_to(message.from_user.id, CHANNELS_IDS)
		if not is_subscribed:
			# TODO: handle more exceptions..
			# TODO: Custom callback data decompression error..
			await bot.send_message(
				message.chat.id, 'Подпишись на каналы:',
				reply_markup=keyboard_channels_links_list,
			)
		return is_subscribed
