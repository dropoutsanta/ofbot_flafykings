from threading import Thread
from handlers.gptHandler import updatePersonalityGPT

from handlers.supabaseHandler import getPersonality, postPersonality

def updatePersonality(chatId, bot_id, userMessage):
    resume = 'User said: "' + userMessage + '"'

    currentPersonality = getPersonality(chatId, bot_id)
    updatedPersonality = updatePersonalityGPT(currentPersonality, resume)
    postPersonality(updatedPersonality, chatId, bot_id)

# Define a new function to handle this in a new thread
def updatePersonalityAsync(chatId, botId, userMessage):
    Thread(target=updatePersonality, args=(chatId, botId, userMessage)).start()