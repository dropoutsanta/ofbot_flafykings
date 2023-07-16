import requests
import json

def getFunctions():
    functions = [
            {
                "name": "request",
                "description": "When the user requests something from you",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "classify": {
                            "type": "string",
                            "description": """Classify between the following categories. Send back one of the key. Only answer with one of the following keys.
    Misc: is a picture of anything other than you
    SFW: is a selfie of you
    SFW+: is a sexy picture of you where you are wearing clothes
    NSFW: is a nude picture of you
    NSFW+: is a video of you having sex""",
                        },
                        "mediacaption": {
                            "type": "string",
                            "description": """The text to go along with the media you are sending. Include lot's of emojies.""",
                        }
                    },
                    "required": ["classify", "mediacaption"],
                },
            },
            {
                "name": "question",
                "description": "Every time the user asks you a question you call this function answer the question and ask a new one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "assistantResponse": {
                            "type": "string",
                            "description": "The answer to the question",
                        },
                        "assistantQuestion": {
                            "type": "string",
                            "description": "The question you want to ask the user. You are also curious",
                        }
                    },
                    "required": ["assistantResponse", "assistantQuestion" ],
                },
            },
            {
                "name": "compliments",
                "description": "When the user compliments you call this function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "thankyou": {
                            "type": "string",
                            "description": "Thank the user for the compliment",
                        },
                        "compliment": {
                            "type": "string",
                            "description": "Either ask a question or compliment the user using the context",
                        }
                    },
                    "required": ["thankyou", "compliment"],
                },
            },
            {
                "name": "user_info",
                "description": "When the user provides information about himself call this function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answerUser": {
                            "type": "string",
                            "description": "Answer the user with a compliment if you can",
                        },
                        "assistantQuestion": {
                            "type": "string",
                            "description": "After responding ask a new question to the user",
                        },
                    },
                    "required": ["answerUser", "assistantQuestion"],
                },
            },
            {
                "name": "offer",
                "description": "when the user makes you a money offer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The user input",
                        }
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "unknown",
                "description": "When you don't understant the user input or what the user id trying to say",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The user input",
                        }
                    },
                    "required": ["text"],
                },
            },
        ]
    return functions

def getSystemMessage():
    url = "https://citeifmttmdotbcsotyh.supabase.co/rest/v1/bots?id=eq.2"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    result = jsonValue[0]['system_message']
    return result

def getAPIKey():
    url = "https://citeifmttmdotbcsotyh.supabase.co/rest/v1/bots?id=eq.2"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    result = jsonValue[0]['telegram_API_key']
    return result

def getSystemMessage(bot_id):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/bots?id=eq.{bot_id}"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    result = jsonValue[0]['system_message']
    return result

def getAllKeys():
    url = "https://citeifmttmdotbcsotyh.supabase.co/rest/v1/bots"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_text = response.text
    jsonValue = json.loads(response_text)
    allValues = []
    for item in jsonValue:
        result = {
            "id": item["id"],
            "system_message": item["system_message"],
            "telegram_API_key": item["telegram_API_key"]
        }
        allValues.append(result)

    print(allValues)
    
    return allValues
    

getAllKeys()