import os

DB_USERNAME = os.getenv('DB_USERNAME', 'Donald')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')
DB_URL = os.getenv('DB_URL', "localhost:8889/newdb")
