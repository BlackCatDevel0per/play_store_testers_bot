from aiogram import F
from aiogram.filters import MagicData

from data.config import ADMINS

filter_access_admins = MagicData(F.event.from_user.id.in_(ADMINS))
