from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
professors_name = ["professor1" , "professor2" , "professor3"]
lessons = ["1", "2", "3"]

async def profFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Choose a professor" , switch_inline_query_current_chat="#professors")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to choose a professor:", reply_markup=reply)
    
async def lessonFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Choose a lesson" , switch_inline_query_current_chat="#lessons")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the button below to choose a lesson:", reply_markup=reply)
    
async def inlineQuery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query.lower()
    if query.startswith("#professors"):
        keyword = query[len("#professors"):].strip()
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=professor,
                input_message_content=InputTextMessageContent(professor),
            )
            for professor in professors if keyword in professor.lower()
        ]
        await update.inline_query.answer(results)
    elif query.startswith("#lessons"):
        keyword = query[len("#lessons"):].strip()
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=lesson,
                input_message_content=InputTextMessageContent(lesson),
            )
            for lesson in lessons if keyword in lesson.lower()
        ]
        await update.inline_query.answer(results)
        
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