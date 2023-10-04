from handlers.chatHandler import handleMessage
from handlers.responseHandler import sendVideo
from handlers.supabaseHandler import postUser
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functools import partial

from classes.User.User import User

def setupBot(botData):
    botToken = botData['telegram_API_key']
    systemMessage = botData['system_message']
    botId = botData['id']

    # Instantiate a Telegram Bot object
    bot = Bot(token=botToken)
    updater = Updater(token=botToken, use_context=True)
    dispatcher = updater.dispatcher 
    videoHandler = CommandHandler('video', sendVideo)
    startHandler = CommandHandler('start', partial(start, botId))
    messageHandler = MessageHandler(Filters.text & (~Filters.command), partial(handleMessage, botId))
 

    dispatcher.add_handler(startHandler)
    dispatcher.add_handler(messageHandler)
    dispatcher.add_handler(videoHandler)

    updater.start_polling()

    return updater

def start(bot_id,update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello!')
    print("starting bot")
    user = update.message.from_user
    print("Got a User - information:", user)
    userObject = User(user.id, user.username, user.first_name, user.last_name, user.language_code, bot_id)
    postUser(userObject)