from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from uuid import uuid4

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    
professors_name = ["professor1" , "professor2" , "professor3"]
lessons = ["1", "2", "3"]

async def mainFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
    [InlineKeyboardButton("Choose your professor", switch_inline_query_current_chat="#professors"),
     InlineKeyboardButton("Choose your lesson", switch_inline_query_current_chat="#lessons")]
    ]
    reply = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the buttons below to choose a professor or a lesson:", reply_markup=reply)
    
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
            for professor in professors_name if keyword in professor.lower()
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