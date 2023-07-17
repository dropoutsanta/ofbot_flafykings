import openai
import requests
import json
import os

openAIKey = os.environ.get('OPEN_AI_KEY')

def upDatePersonalityGPT(personality, newText):
    messages = [
         {
    "role": "system",
    "content": f"""You are given a current user personality traits and a new messages,
you need to update the user personality with the information in the last message. Only add personality traits and nothing else. Make it small and consice

User personality: {personality}

New message: {newText}
Updated personality:"""
    }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    response_message = response["choices"][0]["message"]['content']
    print("LLM OUT PERSONALITY")
    print(response_message)
    return response_message
    

def updatePersonalityDB(personality, userId, bot_id):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/users?user_id=eq.{userId}&bot_id=eq.{bot_id}" 

    payload = json.dumps({
    "conversation_personality": personality
    })
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.text)


def getPersonality(chatId, bot_id):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/users?user_id=eq.{chatId}&bot_id=eq.{bot_id}"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    print(jsonValue)
    result = jsonValue[0]['conversation_personality']
    print("USER PERSONALITY")
    print(result)
   
    return result

