from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from uuid import uuid4

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

user_selection = {}
professors_name = ["professor1" , "professor2" , "professor3"]
lessons = ["1", "2", "3"]

async def mainFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    if user_id not in user_selection:
        user_selection[user_id] = {"selected_professor": None, "selected_lesson": None}

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
        
async def selectionHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = update.message.text.strip()

    if user_id not in user_selection:
        user_selection[user_id] = {"selected_professor": None, "selected_lesson": None}

    if message in professors_name:
        if user_selection[user_id]["selected_professor"]:
            await update.message.reply_text(
                f"You've already selected {user_selection[user_id]['selected_professor']} as your professor. Do you want to change it? Reply with 'reset selection' to reset your selection."
            )
        else:
            user_selection[user_id]["selected_professor"] = message
            await update.message.reply_text(f"You selected {message} as your professor.")

    elif message in lessons:
        if user_selection[user_id]["selected_lesson"]:
            await update.message.reply_text(
                f"You've already selected {user_selection[user_id]['selected_lesson']} as your lesson. Do you want to change it? Reply with 'reset selection' to reset your selection."
            )
        else:
            user_selection[user_id]["selected_lesson"] = message
            await update.message.reply_text(f"You selected {message} as your lesson.")

    elif message.lower() == "reset selection":
        user_selection[user_id] = {"selected_professor": None, "selected_lesson": None}
        await update.message.reply_text("Selections reset. You can choose again.")
        