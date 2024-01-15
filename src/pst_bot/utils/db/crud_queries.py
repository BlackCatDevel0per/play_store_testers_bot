from sqlalchemy import func, select

from .tables import AppsTicketsTable, UsersTable

# ...
query__users__user_id = select(UsersTable.user_id)

query_count__users__users_ids = select(func.count(UsersTable.user_id))


query__apps_tickets__app_url = select(AppsTicketsTable.app_url)
