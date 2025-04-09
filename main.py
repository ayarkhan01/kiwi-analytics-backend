import pymysql
pymysql.install_as_MySQLdb()
from services.user_dao import password_match

password_match('admin', 'admin')
