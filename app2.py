from telegram import Bot, Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from gpt2 import callGPT
from checkResponse import check_response_type
from telegram import InputFile
import random
import json
from superbase import sendToDB
from chatSummary import upDateSummaryGPT, getSummary, updateSummaryDB
from createUser import createUser
from botVariables import getSystemMessage, getAPIKey, getAllKeys
from functools import partial
from getImages import getSFW




# Instantiate a Telegram Bot object
bot_token = getAPIKey()
bot = Bot(token=bot_token)

def send_image(update: Update, context: CallbackContext, img_path) -> None:
    chat_id = update.message.chat_id
    with open(img_path, 'rb') as file:
        context.bot.send_photo(chat_id=chat_id, photo=InputFile(file))
def send_image_url(update: Update, context: CallbackContext, img_url: str) -> None:
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=img_url)
def send_video(update, context, vid_path):
    chat_id = update.message.chat_id
    context.bot.send_video(chat_id=chat_id, video=open(vid_path, 'rb'))


def start(bot_id,update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')
    user = update.message.from_user
    print("USER")
    print(user)
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    language_code = user.language_code
    createUser(user_id, username, first_name, last_name, language_code, bot_id)

def updateDatabaseAndSummary(chatId, message, senderType, bot_id):
    sendToDB(chatId, message, senderType, bot_id)
    resumeText = f"Kate said: {message}"
    summary = getSummary(chatId, bot_id)
    newSummary = upDateSummaryGPT(summary, resumeText)
    print(newSummary)
    summaryDBResult = updateSummaryDB(newSummary, chatId, bot_id)

# Define a new function to handle this in a new thread
def updateDatabaseAndSummaryAsync(chatId, message, senderType, bot_id):
    Thread(target=updateDatabaseAndSummary, args=(chatId, message, senderType, bot_id)).start()

def updateUserMessageAndSummary(chatId, message, senderType, bot_id, resumeText):
    sendToDB(chatId, message, senderType, bot_id)
    summary = getSummary(chatId, bot_id)
    print("SUMMARY")
    print(summary)
    # Get new summary
    newSummary = upDateSummaryGPT(summary, resumeText)
    print(newSummary)
    summaryDBResult = updateSummaryDB(newSummary, chatId, bot_id)

# Define a new function to handle this in a new thread
def updateUserMessageAndSummaryAsync(chatId, message, senderType, bot_id, resumeText):
    Thread(target=updateUserMessageAndSummary, args=(chatId, message, senderType, bot_id, resumeText)).start()


def handle_message(bot_id, update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    user = update.message.from_user
    first_name = user.first_name
    last_name = user.last_name
    # This function will be called whenever the bot receives a message.
    text = update.message.text
    resumeText = f"{first_name} said: {text}"
    chat_id = update.message.chat_id
    updateUserMessageAndSummaryAsync(chatId=chat_id, message=text, senderType="user", bot_id=bot_id, resumeText=resumeText)
    
    systemMessage = getSystemMessage(bot_id=bot_id)
    if "conversation" not in context.chat_data:
        context.chat_data["conversation"] = [
            {
                "role": "system",
                "content":systemMessage},
        ]
    systemAndLastFourMessages = []
    
    context.chat_data["conversation"].append({"role": "user", "content": text})

    # Prepare the API prompt using the conversation history.
    prompt = '\n'.join(item["content"] for item in context.chat_data["conversation"][4:])
    
    messages = context.chat_data["conversation"][-10:][1:]
    print("MESSAGES")
    print(messages)
    for message in messages:
        systemAndLastFourMessages.append(message)

    print("MESSAGES SENT")
    print(systemAndLastFourMessages)
    

    result = callGPT(systemAndLastFourMessages, chat_id, bot_id=bot_id)
    print(result)
    response_type = check_response_type(result)
    if response_type == 1:
        print("1")
        classify_key = result['request']
        if classify_key == "SFW":
            
            pictures = getSFW(bot_id)
            picture_obj = random.choice(pictures)
            picture = picture_obj["url"]
            send_image_url(update, context, picture)  # send the image
            
        if classify_key == "SFW+":
            pictures = getSFW(bot_id)
            picture_obj = random.choice(pictures)
            picture = picture_obj["url"]
            send_image_url(update, context, picture)  # send the image
            
            
        if classify_key == "NSFW":
            randum_num = random.randint(1, 1)
            img_path = f"naked/{str(randum_num)}.jpeg"
            send_image(update, context, img_path)  # send the image
            
        if classify_key == "NSFW+":
            send_video(update, context, 'ericafucking.mp4')
            
            
        mediacaption = result['mediacaption']
        update.message.reply_text(mediacaption)
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=ai_text, senderType="assistant", bot_id=bot_id)




    
    elif response_type == 2:
        print("2")
        loaded = json.loads(result)
        ai_text = loaded['content']
        update.message.reply_text(ai_text)
        sendToDB(chatId=chat_id, message=ai_text, senderType="assistant", bot_id=bot_id)
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})
        resumeText = f"Kate said: {ai_text}"
        summary = getSummary(chat_id, bot_id)
        newSummary = upDateSummaryGPT(summary, resumeText)
        print(newSummary)
        summaryDBResult = updateSummaryDB(newSummary, chat_id, bot_id)

    elif response_type == 3:

        print("3") 
        assistantResponse = result['assistantResponse']
        assistantQuestion = result['assistantQuestion']
       
        update.message.reply_text(assistantResponse)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=userQuestion, senderType="assistant", bot_id=bot_id)
        sendToDB(chatId=chat_id, message=assistantQuestion, senderType="assistant", bot_id=bot_id)
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantResponse})
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
        resumeText = f"Kate said: {assistantResponse} and {assistantQuestion}"
        summary = getSummary(chat_id, bot_id)
        newSummary = upDateSummaryGPT(summary, resumeText)
        print(newSummary)
        summaryDBResult = updateSummaryDB(newSummary, chat_id, bot_id)
        
    elif response_type == 4:
        print("4")
        thankyou = result['thankyou']
        compliment = result['compliment']
        update.message.reply_text(thankyou)
        update.message.reply_text(compliment)
        sendToDB(chatId=chat_id, message=thankyou, senderType="assistant", bot_id=bot_id)
        sendToDB(chatId=chat_id, message=compliment, senderType="assistant", bot_id=bot_id)
        context.chat_data["conversation"].append({"role": "assistant", "content": thankyou})
        context.chat_data["conversation"].append({"role": "assistant", "content": compliment})
        resumeText = f"Kate said: {thankyou} and {compliment}"
        summary = getSummary(chat_id, bot_id)
        newSummary = upDateSummaryGPT(summary, resumeText)
        print(newSummary)
        summaryDBResult = updateSummaryDB(newSummary, chat_id, bot_id)
    elif response_type == 5:
        answerUser = result['answerUser']
        assistantQuestion = result['assistantQuestion']
        update.message.reply_text(answerUser)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=answerUser, senderType="assistant", bot_id=bot_id)
        sendToDB(chatId=chat_id, message=assistantQuestion, senderType="assistant", bot_id = bot_id)
        context.chat_data["conversation"].append({"role": "assistant", "content": answerUser})
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
        resumeText = f"Kate said: {answerUser} and {assistantQuestion}"
        summary = getSummary(chat_id, bot_id)
        newSummary = upDateSummaryGPT(summary, resumeText)
        print(newSummary)
      
        summaryDBResult = updateSummaryDB(newSummary, chat_id, bot_id)

    elif response_type == 6:
        send_video(update, context, 'erica.mp4')
        ai_text = result['offer']
        update.message.reply_text(ai_text)
        sendToDB(chatId=chat_id, message=ai_text, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})
        resumeText = f"Kate said: {ai_text}"
        summary = getSummary(chat_id, bot_id)
        newSummary = upDateSummaryGPT(summary, resumeText)
        print(newSummary)
        summaryDBResult = updateSummaryDB(newSummary, chat_id, bot_id)
    elif response_type == 7:
        update.message.reply_text("?")
        context.chat_data["conversation"].append({"role": "assistant", "content": "?"})
   

    elif response_type == 0:
        ai_text = "error"
        update.message.reply_text(ai_text)
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})

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
updaters = []

def add_updater(updater):
    global updaters
    updaters.append(updater)

if __name__ == "__main__":
    # Fetch all the API keys and system messages
    result = getAllKeys()
    print("RESULTSSSS")
    print(result)
    bot_data = [{'api_key': row['telegram_API_key'], 'system_message': row['system_message'], 'id': row['id']} for row in result]

    # Setup a bot for each token
    for bot in bot_data:
        print(bot)
        bot_id = bot['id']
        updater = setup_bot(bot)
        add_updater(updater)
        


