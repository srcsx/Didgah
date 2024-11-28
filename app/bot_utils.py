from telegram.ext import ApplicationBuilder, CommandHandler
from config.init import TELEGRAM_BOT_TOKEN
from config.constants import START_COMMAND
from .bot_handlers import startCommand

def run():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    setHandlers(app)

    print("The Bot is about to start.")
    app.run_polling()

def setHandlers(app):
    app.add_handler(CommandHandler(START_COMMAND, startCommand))