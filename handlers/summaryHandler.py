from threading import Thread
from handlers.gptHandler import updateSummaryGPT

from handlers.supabaseHandler import getSummary, postSummary


def updateSummary(chatId, bot_id, userMessage, replyMessage, mediaUrl):
    if replyMessage == None:  replyMessage = ''
    if mediaUrl == None:  mediaUrl = ''

    resume = 'User said: "' + userMessage + '" and Kate replied: "' + replyMessage + '"'

    if mediaUrl:
        resume += ' Kate also sent: ' + mediaUrl + ' to the user'

    currentSummary = getSummary(chatId, bot_id)

    updatedSummary = updateSummaryGPT(currentSummary, resume)
 
    postSummary(updatedSummary, chatId, bot_id)

# Define a new function to handle this in a new thread
def updateSummaryAsync(chatId, botId, userMessage, replyMessage, mediaUrl):
    Thread(target=updateSummary, args=(chatId, botId, userMessage, replyMessage, mediaUrl)).start()