import pymysql
pymysql.install_as_MySQLdb()
from services.user_dao import get_active

users = get_active()
for user in users:
    print(user.username, user.password, user.balance)