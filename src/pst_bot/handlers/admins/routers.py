from aiogram import Router
from filters import filter_access_admins

admins_router = Router(name='admins_router')

admins_router.message.filter(filter_access_admins)
admins_router.callback_query.filter(filter_access_admins)
