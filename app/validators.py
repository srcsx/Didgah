from telegram import Update
from telegram.ext import ContextTypes
from config.init import TELEGRAM_VERIFY_GROUP_ID


async def isUserInVerifiedGroup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
	user_id = update.message.from_user.id
	chat_id = "-100" + TELEGRAM_VERIFY_GROUP_ID # Note that -100 in the beginning is to identify that this is a GROUP id. (If you remove it, it won't work)
	try:
		if (await context.bot.getChatMember(chat_id,user_id)): # this line throws an exception when user isn't in the group
			return True
		return False
	except Exception as e:
		if repr(e) == "BadRequest('Participant_id_invalid')":
			return False
		raise e

