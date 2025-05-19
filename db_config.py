# db_config.py

import os

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  # fallback local dev ke liye
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root123')
MYSQL_DB = os.getenv('MYSQL_DB', 'store_inventory')


#MYSQL_HOST = 'localhost'
#MYSQL_USER = 'root'
#MYSQL_PASSWORD = 'root123'
#MYSQL_DB = 'store_inventory'

# db_config.py
#MYSQL_HOST = 'localhost'
#MYSQL_USER = 'your_username'
#MYSQL_PASSWORD = 'your_password'
#MYSQL_DB = 'inventory_db'
