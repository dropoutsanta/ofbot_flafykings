from telegram import Bot, Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def setup_bot(bot_data):
    bot_token = bot_data['api_key']
    system_message = bot_data['system_message']
    bot_id = bot_data['id']

    # Instantiate a Telegram Bot object
    bot = Bot(token=bot_token)

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    video_handler = CommandHandler('video', send_video)
    
    start_handler = CommandHandler('start', partial(start, bot_id))

    
    message_handler = MessageHandler(Filters.text & (~Filters.command), partial(handle_message, bot_id))

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(video_handler)

    updater.start_polling()

    return updater