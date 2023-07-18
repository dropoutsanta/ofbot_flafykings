import openai
import json
import os
from botVariables import getFunctions,getSystemMessage
from chatSummary import getSummary
from superbase import getLastMessages

openAIKey = os.environ.get('OPEN_AI_KEY')
openai.api_key = openAIKey



def callGPT(chatId, bot_id):
    result = run_conversation(chatId, bot_id)
    return result

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def request(classify, mediacaption):
     """Get the current weather in a given location"""
     result = {
     "request": classify,
     "mediacaption": mediacaption
     }
     print("REQUEST")
     print(classify)

     return json.dumps(result)
      

def question(assistantResponse, assistantQuestion):
     """Get the current weather in a given location"""
     result = {
     "assistantResponse": assistantResponse,
     "assistantQuestion": assistantQuestion,

     }
     print("QUESTION")
     

     return json.dumps(result)

def compliment(thankyou,compliment):
     """Get the current weather in a given location"""
     result = {
     "thankyou": thankyou,
     "compliment": compliment
     }
     print("COMPLIMENT")
     

     return json.dumps(result)

def userInfo(answerUser, assistantQuestion):
     """Get the current weather in a given location"""
     result = {
     "answerUser": answerUser,
     "assistantQuestion": assistantQuestion
     }
     print("USER INFO")
     return json.dumps(result)

def offer(text):
     """Get the current weather in a given location"""
     result = {
     "offer": text
     }
     print("OFFER")
     

     return json.dumps(result)
def unknown(text):
     """Get the current weather in a given location"""
     result = {
     "unknown": text
     }
     print("UNKNOWN")
     return json.dumps(result)

def run_conversation(chatId, bot_id):
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "Send a picture"}]
    messages = getLastMessages(chatId, bot_id)
    systemMessage = getSystemMessage(bot_id=bot_id)
    summaryText = getSummary(chatId, bot_id)
   
    
    allMessages = [
            {
                "role": "system",
                "content":systemMessage},
        ]
    for message in messages:
        allMessages.append(message)
    
    functions = getFunctions()
    print("GOING IN THE MODEL FINAL")
    print(allMessages)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=allMessages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    
    response_message = response["choices"][0]["message"]
    total_tokens = response['usage']['total_tokens']
    
    
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "request": request,
            "question": question,
            "compliments": compliment,
            "user_info": userInfo,
            "offer": offer
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_name)
        if function_name == "request":
            function_response = fuction_to_call(
            classify=function_args.get("classify"),
            mediacaption=function_args.get("mediacaption")
        )
        if function_name == "question":
            function_response = fuction_to_call(
            assistantResponse=function_args.get("assistantResponse"),
            assistantQuestion=function_args.get("assistantQuestion"),
        )
        if function_name == "compliments":
            function_response = fuction_to_call(
            thankyou=function_args.get("thankyou"),
            compliment=function_args.get("compliment"),
        )
        if function_name == "user_info":
            function_response = fuction_to_call(
            answerUser=function_args.get("answerUser"),
            assistantQuestion=function_args.get("assistantQuestion"),
        )
       
        return json.loads(function_response), total_tokens

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response
    else: 
        return json.dumps(response_message), total_tokens


