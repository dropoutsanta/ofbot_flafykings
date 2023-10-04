from handlers.gptHandler import callGPT
from handlers.personalityHandler import updatePersonalityAsync
from handlers.responseHandler import checkResponseType, handleAnswerUser, handleAsistantResponse, handleCompliment, handleDefault, handleError, handleOffer, handleRequest, handleUnknown
from handlers.summaryHandler import updateSummaryAsync
from handlers.supabaseHandler import getSystemMessage, postMessage
from telegram import ChatAction, Update
from telegram.ext import CallbackContext

# This function will be called whenever the bot receives a message
def handleMessage(botId, update: Update, context: CallbackContext) -> None:
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    chatId = update.message.chat_id

    userInput = update.message.text
    if "conversation" not in context.chat_data: context.chat_data["conversation"] = [getSystemMessage(botId)]

    context.chat_data["conversation"].append({"role": "user", "content": userInput})
    postMessage(chatId=chatId, message=userInput, senderType="user", botId=botId, tokensUsed=0, mediaUrl=None)
    updatePersonalityAsync(chatId=chatId, userMessage=userInput, botId=botId)
 
    message = context.chat_data["conversation"]
    chatId = update.message.chat_id
    gptReply = callGPT(chatId, botId, message)

    if("secondResponse" in gptReply):
        print("Got a second response - switching result to original response")
        gptReply = gptReply["firstResponse"]

    usage, message = gptReply['usage'], gptReply['message']

    mediaUrl = ''
    replyMessage = message['content']
    responseType = checkResponseType(message)

    if responseType == 1: mediaUrl, replyMessage = handleRequest(message, update, context, botId)
    elif responseType == 2: replyMessage = handleDefault(message, update, context)
    elif responseType == 3: handleAsistantResponse(message, update, context)
    elif responseType == 4: replyMessage = handleCompliment(message, update, context)
    elif responseType == 5: handleAnswerUser(message, update, context)
    elif responseType == 6: replyMessage = handleOffer(message, update, context)
    elif responseType == 7: handleUnknown(message, update, context)
    elif responseType == 0: handleError(message, update, context)
    if replyMessage:
        context.chat_data["conversation"].append({"role": "assistant", "content": replyMessage})
        print(context.chat_data["conversation"])
    print("REPLY MESSAGE: ", replyMessage)
    postMessage(chatId=chatId, message=replyMessage, senderType="assistant", botId=botId, tokensUsed=usage, mediaUrl=mediaUrl)
    updateSummaryAsync(chatId=chatId, userMessage=userInput, replyMessage=replyMessage, mediaUrl=mediaUrl, botId=botId)
 