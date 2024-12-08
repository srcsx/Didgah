from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from uuid import uuid4
from validators import isUserInVerifiedGroup
from config.init import TELEGRAM_SHARE_GROUP_ID
from database.query.prof import selectAllProfs
from database.query.course import selectAllCourses
from database.query.comment import createComment

def getProfessors() -> dict:
    try:
        return {prof.name: prof.id for prof in selectAllProfs()}
    except Exception as e:
        print(f"Failed to fetch professors: {e}")
        return {}
    
def getLessons() -> dict:
    try:
        return {lesson.name: lesson.id for lesson in selectAllCourses()}
    except Exception as e:
        print(f"Failed to fetch lessons: {e}")
        return {}

def initializeUser(user_id: int) -> None:
    if user_id not in user_data:
        user_data[user_id] = {
            "verified": False,
            "selected_professor": None,
            "selected_lesson": None,
            "awaiting_comment": False,
            "comment": None
        }
        
professors = getProfessors()
lessons = getLessons()
user_data = {}
professors_name = list(getProfessors().keys())
lessons_name = list(getLessons().keys())

async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    initializeUser(user_id)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    #TODO need to check if user already exist in database
    if isUserInVerifiedGroup(update , context):
        user_data[user_id]["verified"] = True
        await mainFlow(update , context)
    else:
        user_data[user_id]["verified"] = False
        await update.message.reply_text("Please first join the channel.")

async def mainFlow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main menu interaction to select professor, lesson, or comment."""
    user_id = update.message.from_user.id
    initializeUser(user_id)
    
    if not user_data[user_id]["verified"]:
        await update.message.reply_text("Please first join the channel.")
        return
    
    keyboard = [
        [InlineKeyboardButton("Choose your professor", switch_inline_query_current_chat="#professors"),
         InlineKeyboardButton("Choose your lesson", switch_inline_query_current_chat="#lessons")],
        [InlineKeyboardButton("Comment", callback_data="comment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click the buttons below to choose a professor or a lesson:", reply_markup=reply_markup)
    
async def inlineQuery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles inline queries for professor and lesson selection."""
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
            for lesson in lessons_name if keyword in lesson.lower()
        ]
        await update.inline_query.answer(results)

async def handleProfessorSelection(update: Update, user_id: int, professor_name: str) -> None:
    if user_data[user_id]["selected_professor"]:
        await update.message.reply_text(
            f"You've already selected {user_data[user_id]["selected_professor"]} as your professor. "
            "Reply with 'reset selection' to reset your choices."
        )
    else:
        user_data[user_id]["selected_professor"] = professor_name
        await update.message.reply_text(f"You selected {professor_name} as your professor.")
        
async def handleLessonSelection(update: Update, user_id: int, lesson_name: str) -> None:
    if user_data[user_id]["selected_lesson"]:
            await update.message.reply_text(
                f"You've already selected {user_data[user_id]['selected_lesson']} as your lesson. "
                "Reply with 'reset selection' to reset your choices."
            )
    else:
        user_data[user_id]["selected_lesson"] = lesson_name
        await update.message.reply_text(f"You selected {lesson_name} as your lesson.")
        
async def resetUserSelection(update: Update, user_id):
    user_data[user_id].update({"selected_professor": None, "selected_lesson": None})
    await update.message.reply_text("Selections reset. You can choose again.")
        
async def sendCommentToGroup(updata: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    msg = (
            f"New comment!:\n\n"
            f"Professor: {user_data[user_id]["selected_professor"]}\n"
            f"Lesson: {user_data[user_id]["selected_lesson"]}\n"
            f"Comment: {user_data[user_id]["comment"]}\n"
        )
    await context.bot.send_message(chat_id=TELEGRAM_SHARE_GROUP_ID, text=msg, parse_mode="Markdown")
         
async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles regular text messages and processes user comments and selections."""
    user_id = update.message.from_user.id
    initializeUser(user_id)
    
    if not user_data[user_id]["verified"]:
        await update.message.reply_text("Please first join the channel.")
        return

    message = update.message.text.strip()

    if message in professors:
        handleProfessorSelection(update, user_id, message)
    elif message in lessons:
        handleLessonSelection(update, user_id, message)
    elif message.lower() == "reset selection":
        resetUserSelection(update, user_id)
    elif user_data[user_id]["awaiting_comment"] and user_data[user_id]["selected_professor"] and user_data[user_id]["selected_lesson"]:
        user_data[user_id]["comment"] = message
        user_data[user_id]["awaiting_comment"] = False
        await sendCommentToGroup(update,context,user_id)
        await createComment(professors[user_data[user_id]["selected_professor"]], lessons[user_data[user_id]["selected_lesson"], user_data[user_id]["comment"], user_id])
        await update.message.reply_text("Your comment has been saved.")
        del user_data[user_id]
    else :
        await update.message.reply_text("Your command in not recognized.")
    
async def CommentHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    user = user_data.get(user_id, {})
    if user.get("selected_professor") and user.get("selected_lesson"):
        await query.message.reply_text("Write your comment:")
        user["awaiting_comment"] = True
    else:
        await query.message.reply_text("Please select a professor and a lesson before commenting.")
            
async def unknownHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I didn't understand that.")