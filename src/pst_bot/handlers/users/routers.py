from aiogram import Router
# from filters import UserSubscribed

users_router = Router(name='users_router')  ##name

subed_users_router = Router(name='subscribed_users_router')

# subed_users_router.message.filter(UserSubscribed())
# subed_users_router.callback_query.filter(UserSubscribed())##
##
