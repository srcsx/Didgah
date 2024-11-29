from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
async def profNameFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    professors_name = ["professor1" , "professor2" , "professor3"]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)] for name in professors_name
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a professor:", reply_markup=reply)
    
async def lessonNameFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lessons = ["1" , "2" , "3"]
    keyboard = [
        [InlineKeyboardButton(lesson, callback_data=lesson)] for lesson in lessons
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a lesson:", reply_markup=reply)
    
async def FlowButtonHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_name = query.data
    await query.edit_message_text(f"You selected: {selected_name}")