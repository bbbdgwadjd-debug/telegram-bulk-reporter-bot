import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
DB_NAME = os.getenv('DB_NAME', 'reporter_bot.db')

# Settings
DEFAULT_DELAY = 1.0
REQUEST_TIMEOUT = 30
