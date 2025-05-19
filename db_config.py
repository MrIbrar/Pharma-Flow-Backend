# db_config.py

import os

DB_HOST = os.getenv('DB_HOST', 'ballast.proxy.rlwy.net')  # fallback local dev ke liye
DB_PORT = os.getenv('DB_PORT', '31075')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'GwiJdzlvWwYQQqTCgzJUphdnORjmRxHq')
DB_NAME = os.getenv('DB_NAME', 'railway')


#MYSQL_HOST = 'localhost'
#MYSQL_USER = 'root'
#MYSQL_PASSWORD = 'root123'
#MYSQL_DB = 'store_inventory'

# db_config.py
#MYSQL_HOST = 'localhost'
#MYSQL_USER = 'your_username'
#MYSQL_PASSWORD = 'your_password'
#MYSQL_DB = 'inventory_db'
