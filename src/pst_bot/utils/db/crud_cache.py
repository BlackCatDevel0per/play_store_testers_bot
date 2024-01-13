from sqlalchemy import func, select

from .tables import UsersTable

# ...
query__users__user_id = select(UsersTable.user_id)

query_count__users__users_ids = select(func.count(UsersTable.user_id))
