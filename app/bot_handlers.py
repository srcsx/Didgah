from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
async def profNameFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    professors_name = ["professor1" , "professor2" , "professor3"]
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"professor:{name}")] for name in professors_name
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a professor:", reply_markup=reply)
    
async def lessonNameFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lessons = ["1", "2", "3"]
    keyboard = [
        [InlineKeyboardButton(lesson, callback_data=f"lesson:{lesson}")] for lesson in lessons
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text("Choose a lesson:", reply_markup=reply)
    
async def FlowButtonHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("professor"):
        selected_prof = query.data.split(":")[1]
        context.user_data["selected_prof"] = selected_prof
        await lessonNameFlow(update, context)
    elif query.data.startswith("lesson"):
        selected_lesson = query.data.split(":")[1]
        context.user_data["selected_lesson"] = selected_lesson
        await query.edit_message_text(f"You selected lesson {selected_lesson} with professor {context.user_data.get('selected_prof')}")