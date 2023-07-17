import requests
import json

def sendToDB(chatId, message, senderType, bot_id,total_tokens):
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
        "total_tokens": total_tokens
    }

    response = requests.post(supabase_url, headers=supabase_headers, data=json.dumps(payload))

    if response.status_code == 201:
        print('Record has been inserted!')
    else:
        print(f'Error: {response.status_code}, {response.text}')