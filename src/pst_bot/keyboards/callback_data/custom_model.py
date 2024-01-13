from __future__ import annotations

from typing import TYPE_CHECKING
from zlib import compress as zlib_compress
from zlib import decompress as zlib_decompress

from aiogram.filters.callback_data import MAX_CALLBACK_LENGTH, CallbackData
from brotli import compress as brotli_compress
from brotli import decompress as brotli_decompress

if TYPE_CHECKING:
	from typing import Any, Callable, TypeVar

	T = TypeVar('T', bound='CallbackB_ZSData')


# TODO: Cleanup..
class MetaImmutableInstance(type):
	def __call__(cls, *args: Any, **kwargs: Any) -> object:
		instance = super().__call__(*args, **kwargs)
		instance.__class__ = cls
		return instance

	def __setattr__(self, name: str, value: Any) -> None:
		msg = f"cannot assign to attribute '{name}'"
		raise AttributeError(msg)


class BSerializer(metaclass=MetaImmutableInstance):
	compress: Callable[[bytes], bytes] = brotli_compress
	decompress: Callable[[bytes], bytes] = brotli_decompress


class ZSerializer(metaclass=MetaImmutableInstance):
	compress: Callable[[bytes], bytes] = zlib_compress
	decompress: Callable[[bytes], bytes] = zlib_decompress


# TODO: Type hint..
# TODO: Use iptionally from config..
# FIXME: Check if data not correctly serialized | handle more exceptions.. (zlib.error: Error -3 while decompressing data: incorrect header check)
class CallbackB_ZSData(CallbackData, prefix='.'):  # type: ignore

	if TYPE_CHECKING:
		__serializer: BSerializer | ZSerializer

	# TODO: Self-check if used `__init__`: TypeError: BaseModel.__init__() takes 1 positional argument but 2 were given
	def __init_subclass__(cls, **kwargs: Any) -> None:
		cls.__serializer = kwargs.pop('serializer', ZSerializer)
		super().__init_subclass__(**kwargs)

	def pack(self: CallbackB_ZSData) -> str:
		"""Generate callback data string.

		:return: valid callback data for Telegram Bot API
		"""
		result = [self.__prefix__]
		for key, value in self.model_dump(mode="json").items():
			encoded = self._encode_value(key, value)
			if self.__separator__ in encoded:
				vet = (
					f"Separator symbol {self.__separator__!r} can not be used "
					f"in value {key}={encoded!r}"
				)
				raise ValueError(vet)
			result.append(encoded)
		callback_data = self.__separator__.join(result)
		callback_data = self.__serializer.compress(callback_data.encode())
		callback_data = callback_data.decode('latin1')
		if len(callback_data) > MAX_CALLBACK_LENGTH:
			vet = (
				f"Resulted callback data is too long! "
				f"len({callback_data!r}) > {MAX_CALLBACK_LENGTH}"
			)
			raise ValueError(vet)
		return callback_data

	@classmethod
	def unpack(cls: type[T], value: str) -> T:
		"""Parse callback data string."""
		return super().unpack(
			cls.__serializer.decompress(
										value.encode('latin1'),
										).decode(),
		)  # noqa: S301
