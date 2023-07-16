import openai
import openai
import json
import os

openAIKey = os.environ.get('OPEN_AI_KEY')

def upDateSummaryGPT(summary, newText):
    messages = [
         {
    "role": "system",
    "content": f"""You are given a current summary of a conversation and a new message,
you need to update the summary with the information in the last message

Summary: {summary}

New message: {newText}"""
    }
    ]
    second_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    return second_response

def updateSummaryDB(summary):
    url = "https://citeifmttmdotbcsotyh.supabase.co/rest/v1/users?user_id=eq.123"

    payload = json.dumps({
    "conversation_summary": summary
    })
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.text)


def getSummary(chatId):
    url = f"https://citeifmttmdotbcsotyh.supabase.co/rest/v1/users?user_id=eq.{chatId}"

    payload = {}
    headers = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpdGVpZm10dG1kb3RiY3NvdHloIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODk0NTE3MjMsImV4cCI6MjAwNTAyNzcyM30.H_4m6CyhusV_At9_MgBUXX-P3EUu-9TjgzxTmJHPMzw',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.text

