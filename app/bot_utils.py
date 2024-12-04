from telegram.ext import ApplicationBuilder, filters, CommandHandler, InlineQueryHandler, MessageHandler, CallbackQueryHandler
from config.init import TELEGRAM_BOT_TOKEN
from config.constants import START_COMMAND
from .bot_handlers import startCommand, inlineQuery, messageHandler, CommentHandler, unknownHandler

def run():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    setHandlers(app)

    print("The Bot is about to start.")
    app.run_polling()

def setHandlers(app):
    app.add_handler(CommandHandler(START_COMMAND, startCommand))
    app.add_handler(InlineQueryHandler(inlineQuery))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messageHandler))
    app.add_handler(CallbackQueryHandler(CommentHandler, pattern="^comment$"))
    app.add_handler(MessageHandler(filters.COMMAND, unknownHandler))