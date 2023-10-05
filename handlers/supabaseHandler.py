from classes.User.User import User
from variables.supabaseSettings import supabase

def getAllBots():
    response = supabase.table('bots').select("*").execute()

    return response.data

def getBot(botId):
    response = supabase.table('bots').select("*").eq('id', botId).execute()

    return response.data

def getSystemMessage(botId):
    response = supabase.table('bots').select("system_message, autobiography").eq('id', botId).execute()
    bioAndSystemMessage = response.data[0]['system_message'] + " Here is your biography: " + response.data[0]['autobiography']
    return {"role": 'system', "content": bioAndSystemMessage}

def getSummary(chatId, botId):
    response = supabase.table('users').select("conversation_summary").eq('bot_id', botId).eq('user_id', chatId).execute()
    
    return response.data[0] if response.data else ''

def getLastMessages(chatId):
    response = supabase.table('messages').select("*").eq('chat_id', chatId).order('created_at', desc=True).limit(10).execute()
    
    return response.data

def getAutoBio(botId):
    response = supabase.table('bots').select("autobiography").eq('id', botId).execute()

    return response.data[0]['biography'] if response.data else ''

def getMedias(botId):
    response = supabase.table('media').select("*").eq('id', botId).execute()
   
    return response.data

def getMediaByType(botId, fileType):
    response = supabase.table('media').select("*").eq('bot_id', botId).eq('type', fileType).execute()
   
    return response.data

def getPersonality(chatId, botId):
    response = supabase.table('users').select("conversation_personality").eq('bot_id', botId).eq('user_id', chatId).execute()

    return response.data[0]['conversation_personality'] if response.data else ''

def postMessage(chatId, message, senderType, botId,tokensUsed, mediaUrl):
    print(botId)
    payload = {
        "chat_id": chatId,
        "message": message,
        "sender": senderType,
        "bot_id": botId,
        "tokens_used": tokensUsed,
        "media_url": mediaUrl,
    }

    supabase.table('messages').insert(payload).execute()
    
def postSummary(summary, chatId, botId):
    payload = {
        "conversation_summary": summary,
    }

    supabase.table('users').update(payload).eq('user_id', chatId).execute()

def postPersonality(personality, chatId, botId):
    payload = {
        "conversation_personality": personality
    }
    
    supabase.table('users').update(payload).eq('user_id', chatId).execute()

def postUser(user: User):
    payload = {
        "user_id": user.id,
        "first_name": user.firstName,
        "last_name": user.lastName,
        "language_code": user.languageCode,
        "bot_id": user.botId,
    }
    supabase.table('users').insert(payload).execute()

def postBot(telegramApiKey, systemMessage, biography, username):
    payload = {
        "telegram_API_key": telegramApiKey,
        "system_message": systemMessage,
        "autobiography": biography,
        "telegram_username": username
    }
    return supabase.table('bots').insert(payload).execute()

def updateSystemMessage(botId, systemMessage):
    payload = {
        "system_message": systemMessage,
    }
    supabase.table('bots').update(payload).eq('id', botId).execute()

def updateAutobiography(botId, biography):
    payload = {
        "autobiography": biography,
    }
    supabase.table('bots').update(payload).eq('id', botId).execute()