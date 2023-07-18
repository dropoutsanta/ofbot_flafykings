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
from botVariables import getSystemMessage, getAPIKey, getAllKeys, getVoiceOccurance
from functools import partial
from getImages import getSFW
from threading import Thread
from queryVector import queryVectorImage, queryVectorText
from chatMemory import upDateMemoryGPT, getMemory, updateMemoryDB
from chatPersonality import upDatePersonalityGPT, getPersonality, updatePersonalityDB
from gptFormat import formatAnswer
from elevenlabs import generate, set_api_key
from io import BytesIO
import random
import soundfile as sf
import os
import tempfile
import audioread

set_api_key("af592672bccdfbdb8bae883c6fe1d76e") 




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

def updateDatabaseAndSummary(chatId, message, senderType, bot_id, total_tokens, media_url=None, voice_seconds=0):
    sendToDB(chatId, message, senderType, bot_id, total_tokens, media_url, voice_seconds)
    resumeText = f"Kate said: {message}"
    summary = getSummary(chatId, bot_id)
    newSummary = upDateSummaryGPT(summary, resumeText)
    memory = getMemory(chatId, bot_id)
    newMemory = upDateMemoryGPT(memory, resumeText)
    print("MEMORY")
    print(newMemory)
    summaryDBResult = updateSummaryDB(newSummary, chatId, bot_id)
    memoryDBResult = updateMemoryDB(newMemory, chatId, bot_id)

# Define a new function to handle this in a new thread
def updateDatabaseAndSummaryAsync(chatId, message, senderType, bot_id, total_tokens, media_url=None, voice_seconds=0):
    Thread(target=updateDatabaseAndSummary, args=(chatId, message, senderType, bot_id, total_tokens, media_url, voice_seconds)).start()

def updateUserMessageAndSummary(chatId, message, senderType, bot_id, resumeText, total_tokens=0, media_url=None):
    summary = getSummary(chatId, bot_id)
    newSummary = upDateSummaryGPT(summary, resumeText)
    summaryDBResult = updateSummaryDB(newSummary, chatId, bot_id)

    memory = getMemory(chatId, bot_id)
    newMemory = upDateMemoryGPT(memory, message)
    memoryDBResult = updateMemoryDB(newMemory, chatId, bot_id)

    personality = getPersonality(chatId, bot_id)
    newPersonality = upDatePersonalityGPT(personality, message)
    personalityDBResult = updatePersonalityDB(newPersonality, chatId, bot_id)


# Define a new function to handle this in a new thread
def updateUserMessageAndSummaryAsync(chatId, message, senderType, bot_id, resumeText,media_url=None):
    Thread(target=updateUserMessageAndSummary, args=(chatId, message, senderType, bot_id, resumeText, media_url)).start()


def handle_message(bot_id, update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    user = update.message.from_user
    first_name = user.first_name
    last_name = user.last_name
    # This function will be called whenever the bot receives a message.
    text = update.message.text
    resumeText = f"{first_name} said: {text}"
    chat_id = update.message.chat_id
    sendToDB(chatId=chat_id, message=text, senderType="user", bot_id=bot_id, total_tokens=0, media_url=None)
    updateUserMessageAndSummaryAsync(chatId=chat_id, message=text, senderType="user", bot_id=bot_id, resumeText=resumeText)

    result, total_tokens = callGPT(chat_id, bot_id=bot_id)
    print(result)
    print("TOTAL TOKEN")
    print(total_tokens)
    response_type = check_response_type(result)
    if response_type == 1:
        print("1")
        classify_key = result['request']
        if classify_key == "SFW":
            metadata = queryVectorImage(text, bot_id)
            pictures = getSFW(bot_id)
            picture_obj = random.choice(pictures)
            url = metadata['url']
            picture = picture_obj["url"]
            send_image_url(update, context, url)  # send the image
            
        if classify_key == "SFW+":
            
            metadata = queryVectorImage(text, bot_id)
            pictures = getSFW(bot_id)
            picture_obj = random.choice(pictures)
            picture = picture_obj["url"]
            url = metadata['url']
            send_image_url(update, context, url)  # send the image
            
            
        if classify_key == "NSFW":
            metadata = queryVectorImage(text, bot_id)
            url = metadata['url']
            send_image_url(update, context, url)  # send the image
            
        if classify_key == "NSFW+":
            # send_video(update, context, 'ericafucking.mp4')
            metadata = queryVectorImage(text, bot_id)
            url = metadata['url']
            send_image_url(update, context, url) 
            
        
        mediacaption = result['mediacaption']
        update.message.reply_text(mediacaption)
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=mediacaption, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens, media_url=metadata['url'])




    
    elif response_type == 2:
        print("2")
        loaded = json.loads(result)
        ai_text = loaded['content']
        occurance = getVoiceOccurance(bot_id)
        if occurance != 0 and occurance is not None:
            send_voice = random.randint(1, occurance) == 1
            if send_voice:
                # Convert text to speech using Eleven Labs API
                # Convert text to speech using Eleven Labs API
                audio = generate(
                    text=ai_text,
                    voice="Bella", # or whichever voice you want to use, 
                )
                fp = BytesIO(audio)
                fp.name = "response.ogg"
                update.message.reply_voice(voice=fp)
                
                with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                    f.write(fp.getbuffer())
                    temp_name = f.name

                # Use audioread to load the audio file
                with audioread.audio_open(temp_name) as f:
                    length_in_seconds = f.duration
                print("LENGHT IN SEC")
                print(length_in_seconds)

                # Delete the temporary file
                os.remove(temp_name)
                updateDatabaseAndSummaryAsync(chatId=chat_id, message=ai_text, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens, voice_seconds=length_in_seconds)
                
               
            else: 
                update.message.reply_text(ai_text)
                updateDatabaseAndSummaryAsync(chatId=chat_id, message=ai_text, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens)

       
        

    elif response_type == 3:
        print("3")
        questionResponse = queryVectorText(text)
        questionResponseText = questionResponse['text']
        #result2 = formatAnswer(text,questionResponseText)
        #loaded = json.loads(result2)
        #ai_text = loaded['content']
        assistantResponse = result['assistantResponse']
        assistantQuestion = result['assistantQuestion']
        resumeText = f"You said: {assistantResponse} and {assistantQuestion}"
        update.message.reply_text(assistantResponse)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=assistantResponse, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens, media_url=None)
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=assistantQuestion, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens)
        
    elif response_type == 4:
        print("4")
        thankyou = result['thankyou']
        compliment = result['compliment']
        update.message.reply_text(thankyou)
        update.message.reply_text(compliment)
        sendToDB(chatId=chat_id, message=thankyou, senderType="assistant", bot_id=bot_id,total_tokens=total_tokens, media_url=None)
        resumeText = f"You said: {thankyou} and {compliment}"
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=compliment, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens)

    elif response_type == 5:
        answerUser = result['answerUser']
        assistantQuestion = result['assistantQuestion']
        update.message.reply_text(answerUser)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=answerUser, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens, media_url=None)
       
        resumeText = f"You said: {answerUser} and {assistantQuestion}"
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=assistantQuestion, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens)


    elif response_type == 6:
        send_video(update, context, 'erica.mp4')
        ai_text = result['offer']
        update.message.reply_text(ai_text)
       
        resumeText = f"You said: {ai_text}"
        updateDatabaseAndSummaryAsync(chatId=chat_id, message=ai_text, senderType="assistant", bot_id=bot_id, total_tokens=total_tokens)

    elif response_type == 7:
        update.message.reply_text("?")

   

    elif response_type == 0:
        ai_text = "error"
        update.message.reply_text(ai_text)
     

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
    
    bot_data = [{'api_key': row['telegram_API_key'], 'system_message': row['system_message'], 'id': row['id']} for row in result]

    # Setup a bot for each token
    for bot in bot_data:
       
        bot_id = bot['id']
        updater = setup_bot(bot)
        add_updater(updater)
        


