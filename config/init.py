import os

# Telegram bot related configs
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "default")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "default")
TELEGRAM_VERIFY_GROUP_ID = os.getenv("TELEGRAM_VERIFY_GROUP_ID", "default")
TELEGRAM_SHARE_GROUP_ID = os.getenv("TELEGRAM_SHARE_GROUP_ID", "default")

# Database related configs
DATABASE_URL = os.getenv("DATABASE_URL", "default")
