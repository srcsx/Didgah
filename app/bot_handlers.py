from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
async def newComment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    professors_name = ["professor1" , "professor2" , "professor3"]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)] for name in professors_name
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a professor:", reply_markup=reply)
    
async def newCommentClickHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_name = query.data
    await query.edit_message_text(f"You selected: {selected_name}")