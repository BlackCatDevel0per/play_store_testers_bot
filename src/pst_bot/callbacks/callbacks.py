import asyncio
import logging

from aiogram.types.message import Message
from async_class import AsyncObject

logger = logging.getLogger('bot')


class Callbacks(AsyncObject):  # need delete=True or auto_delete=True or which one first del..
	def __init__(self, message: Message, username: str, percentage_step: int = 10, task_sleep: int = 2, *, message_delete_after_complete: bool = True):
		self._AsyncObject__closed = True  # To fix: Exception ignored in: <function AsyncObject.__del__ at 0x7f672daa7ee0>
		self.message = message  # Message for edit
		self.username = username  # Username to show in logs
		self.percentage_step = percentage_step
		self.task_sleep = task_sleep
		self.message_delete_after_complete = message_delete_after_complete

		self.upload_percentage = 0
		self.download_percentage = 0


	# async def __adel__(self):
	# 	if self.message_delete_after_complete:
	# 		await self.message.delete()  # Why not work?!?!?!


	def callback_svs(self, current, total) -> None:
		percentage = int('{:.0%}'.format(current / total)[:-1])
		if percentage % self.percentage_step == 0:
			if percentage != self.upload_percentage:
				self.upload_percentage = percentage


	async def msg_callback_task_svs(self) -> None:
		t = 0
		cf = self.upload_percentage
		while self.upload_percentage <= 100:
			await asyncio.sleep(self.task_sleep)
			if self.upload_percentage != cf:
				# logger.info(f'SVStatus {self.username}: {percentage}')
				await self.message.edit_text(f"Отправка: {self.upload_percentage}%")
				t += self.task_sleep
				cf = self.upload_percentage


	def on_progress_dvs(self, current, total) -> None:
		percentage = int('{:.0%}'.format(current / total)[:-1])
		if percentage % self.percentage_step == 0:
			if percentage != self.download_percentage:
				self.download_percentage = percentage


	async def msg_on_progress_task_dvs(self) -> None:
		t = 0
		cf = self.download_percentage
		while self.download_percentage <= 100:
			await asyncio.sleep(self.task_sleep)
			if self.download_percentage != cf:
				# logger.info(f"DVStatus {self.username}: {percents_}")
				await self.message.edit_text(f"Скачивание: {self.download_percentage}%")
				t += self.task_sleep
				cf = self.download_percentage
