import json
import random
from handlers.supabaseHandler import getMediaByType

from telegram import Update
from telegram.ext import CallbackContext

global replyMessage

def handleRequest(result, update: Update, context: CallbackContext, botId) -> str:
    print("Result for response type 'Request': ", result)

    arguments = json.loads(result.function_call.arguments)
    classify_key = arguments['classify']
    replyMessage = 'Do you like it? :)'

    if classify_key == "SFW" or classify_key == "Misc":
        mediaData = getMediaByType(botId, 'SFW')
        print(mediaData)
        randomPictureNumber = random.randrange(len(mediaData))
        mediaData = mediaData[randomPictureNumber]
        sendImage(update, context, mediaData['url'])
        replyMessage = "Here is my selfie, I hope you like it :)"

    if classify_key == "SFW+":
        mediaData = getMediaByType(botId, 'SFW+')
        print(mediaData)
        randomPictureNumber = random.randrange(len(mediaData))
        mediaData = mediaData[randomPictureNumber]
        sendImage(update, context, mediaData['url'])
        replyMessage = "This one is a little sexy, don't you think? :)"

    if classify_key == "NSFW":
        mediaData = getMediaByType(botId, 'SFW+')
        randomPictureNumber = random.randrange(len(mediaData))
        mediaData = mediaData[randomPictureNumber]
        sendImage(update, context, mediaData['url'])
        replyMessage = "Do you like what you see? :)"

    if classify_key == "NSFWPrelims":
        mediaData = getMediaByType(botId, 'NSFW+')
        randomPictureNumber = random.randrange(len(mediaData))
        mediaData = mediaData[randomPictureNumber]
        sendVideo(update, context, mediaData['url'])
        replyMessage = "Do you like what you see? :)"
        
    if classify_key == "NSFW+":
        mediaData = getMediaByType(botId, 'NSFW+')
        randomPictureNumber = random.randrange(len(mediaData))
        mediaData = mediaData[randomPictureNumber]
        sendVideo(update, context, mediaData['url'])
        replyMessage = "Imagine if you were here :)"


    update.message.reply_text(replyMessage)
    return mediaData['url'], replyMessage


def handleDefault(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'Default': ", result)

    responseText = result['content']
    
    update.message.reply_text(responseText)

    return responseText

def handleAsistantResponse(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'AsistantResponse': ", result)

    arguments = json.loads(result.function_call.arguments)

    userQuestion = arguments['userQuestion']
    assistantQuestion = arguments['assistantQuestion']

    update.message.reply_text("Respond to the question")
    update.message.reply_text(userQuestion)
    update.message.reply_text(assistantQuestion)

    context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})

def handleCompliment(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'Compliment': ", result)

    arguments = json.loads(result.function_call.arguments)

    thankyou = arguments['thankyou']
    compliment = arguments['compliment']

    update.message.reply_text(thankyou)
    update.message.reply_text(compliment)

    resumeText = f"You said: {thankyou} and {compliment}"

    return resumeText

def handleAnswerUser(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'AnswerUser': ", result)

    arguments = json.loads(result.function_call.arguments)

    answerUser = arguments['answerUser']
    assistantQuestion = arguments['assistantQuestion']

    update.message.reply_text(answerUser)
    update.message.reply_text(assistantQuestion)

    context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})

def handleOffer(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'Offer': ", result)

    arguments = json.loads(result.function_call.arguments)

    responseText = arguments['text']
    update.message.reply_text(responseText)
    update.message.reply_text("Here is the link to my OnlyFans: http://www.onlyfans.com")

    return responseText

def handleUnknown(result, update: Update, context: CallbackContext) -> None:
    print("Result for response type 'Unknown': ", result)

    update.message.reply_text("I am sorry babe, I didn't understand your message")

    context.chat_data["conversation"].append({"role": "assistant", "content": "?"})

def handleError(result, update: Update, context: CallbackContext) -> None:
    print("An error occured while handling response type")

    errorText = 'I am sorry, I might have some technical problems right now'
    update.message.reply_text(errorText)

    context.chat_data["conversation"].append({"role": "assistant", "content": errorText})

def checkResponseType(response) -> int:
    if hasattr(response, 'function_call'):
        functionName = response.function_call.name
        if functionName == 'request': return 1
        if functionName == 'assistantResponse': return 3
        if functionName == 'compliments': return 4
        if functionName == 'user_info': return 5
        if functionName == 'offer': return 6
        if functionName == 'unknown': return 7
    elif 'role' in response and 'content' in response:
        return 2
    else:
        return 0
    
# This function will be called whenever the bot sends an image
def sendImage(update: Update, context: CallbackContext, imageUrl) -> None:
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=imageUrl)
        
# This function will be called whenever the bot sends a video
def sendVideo(update: Update, context: CallbackContext, videoUrl) -> None:
    chat_id = update.message.chat_id
    context.bot.send_video(chat_id=chat_id, video=videoUrl)