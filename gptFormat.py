import openai
import json
import os

openAIKey = os.environ.get('OPEN_AI_KEY')
openai.api_key = openAIKey

def formatAnswer(question, context):
    messages = [{
        "role": "system", "content": "You are given a question and a context, answer the question using the context"
    },
    {
        "role": "user", "content": f"""Question: {question}
Context: {context}
Answer:"""
    },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    response_message = response["choices"][0]["message"]
    return json.dumps(response_message)



