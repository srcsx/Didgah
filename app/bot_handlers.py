from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from uuid import uuid4

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

user_data = {}
professors_name = ["professor1" , "professor2" , "professor3"]
lessons = ["1", "2", "3"]

def initializeUser(user_id: int) -> None:
    if user_id not in user_data:
        user_data[user_id] = {
            "selected_professor": None,
            "selected_lesson": None,
            "awaiting_comment": False,
            "comment": None
        }

async def mainFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    initializeUser(user_id)

    keyboard = [
        [InlineKeyboardButton("Choose your professor", switch_inline_query_current_chat="#professors"),
         InlineKeyboardButton("Choose your lesson", switch_inline_query_current_chat="#lessons")],
        [InlineKeyboardButton("Comment", callback_data="comment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the buttons below to choose a professor or a lesson:", reply_markup=reply_markup)
    
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
        
async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles regular text messages and processes user inputs and selections."""
    user_id = update.message.from_user.id
    initializeUser(user_id)

    message = update.message.text.strip()

    if message in professors_name:
        if user_data[user_id]["selected_professor"]:
            await update.message.reply_text(
                f"You've already selected {user_data[user_id]['selected_professor']} as your professor. "
                "Reply with 'reset selection' to reset your choices."
            )
        else:
            user_data[user_id]["selected_professor"] = message
            await update.message.reply_text(f"You selected {message} as your professor.")

    elif message in lessons:
        if user_data[user_id]["selected_lesson"]:
            await update.message.reply_text(
                f"You've already selected {user_data[user_id]['selected_lesson']} as your lesson. "
                "Reply with 'reset selection' to reset your choices."
            )
        else:
            user_data[user_id]["selected_lesson"] = message
            await update.message.reply_text(f"You selected {message} as your lesson.")

    elif message.lower() == "reset selection":
        user_data[user_id].update({"selected_professor": None, "selected_lesson": None})
        await update.message.reply_text("Selections reset. You can choose again.")

    elif user_data[user_id]["awaiting_comment"]:
        user_data[user_id]["comment"] = message
        user_data[user_id]["awaiting_comment"] = False
        await update.message.reply_text("Your comment has been saved.")
    
async def CommentHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if query.data.startswith("comment"):
        if user_data[user_id]["selected_professor"] and user_data[user_id]["selected_lesson"]:
            await query.message.reply_text("Write your comment:")
            user_data[user_id]["awaiting_comment"] = True
        else:
            await query.message.reply_text("Please first select a professor and a lesson to send a comment.")