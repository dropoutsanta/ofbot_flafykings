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


def getSummary():
    pass
