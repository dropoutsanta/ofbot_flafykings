import requests
import json

def sendToDB(chatId, message, senderType, bot_id,total_tokens, media_url, voice_seconds=0):
    supabase_url = 'https://citeifmttmdotbcsotyh.supabase.co/rest/v1/messages'
    supabase_headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
        'Content-Type': 'application/json'
    }

    payload = {
        "chat_id": chatId,
        "message": message,
        "sender": senderType,
        "bot_id": bot_id,
        "tokens_used": total_tokens,
        "media_url": media_url,
        "voice_seconds": voice_seconds
    }

    response = requests.post(supabase_url, headers=supabase_headers, data=json.dumps(payload))

    if response.status_code == 201:
        print('Record has been inserted!')
    else:
        print(f'Error: {response.status_code}, {response.text}')
        
        

def getLastMessages(chatId, bot_id):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/messages?chat_id=eq.{chatId}&bot_id=eq.{bot_id}&order=created_at.desc&limit=10"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    print(jsonValue)
    allMessages = []
    for item in jsonValue:
        message = item.get('message')  # Replace 'message' with the actual field name
        role = item.get('sender')
        obj = {
            "role": role,
            "content": message
        }
        allMessages.append(obj)
    print("SUPERBASE BACK")
    allMessages = allMessages[::-1]  # Reverse the list
    print(allMessages)
    return allMessages
