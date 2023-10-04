from handlers.supabaseHandler import getSummary, getSystemMessage, getLastMessages
import openai
import json
from variables.apiKeys import OPENAI_API_KEY
from variables.gptPromps import handlingFunctions

# Ensure that you've set your OpenAI API key
openai.api_key = OPENAI_API_KEY

def callGPT(chatId, botId, message):
    result = run_conversation(chatId, botId, message)
    return result

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def request(classify):
    result = {
    "request": classify
    }

    return json.dumps(result)
      

def question(userQuestion, assistantQuestion):
    result = {
    "userQuestion": userQuestion,
    "assistantQuestion": assistantQuestion,
    }  

    return json.dumps(result)

def compliment(thankyou,compliment):
    result = {
    "thankyou": thankyou,
    "compliment": compliment
    }

    return json.dumps(result)

def userInfo(answerUser, assistantQuestion):
    result = {
    "answerUser": answerUser,
    "assistantQuestion": assistantQuestion
    }

    return json.dumps(result)

def offer(text):
    result = {
    "offer": text
    }

    return json.dumps(result)
def unknown(text):
    result = {
    "unknown": text
    }

    return json.dumps(result)

def run_conversation(chatId, botId, message):
    # Step 1: send the conversation and available functions to GPT
    firstResponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        functions=handlingFunctions,
    )

    firstResponse = {"usage": firstResponse["usage"]["total_tokens"], "message": firstResponse["choices"][0]["message"]} 
    responseMessage = firstResponse["message"]
    # Step 2: check if GPT wanted to call a function
    if responseMessage.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "request": request,
            "question": question,
            "compliments": compliment,
            "user_info": userInfo,
            "offer": offer,
            "unknown": unknown
        }  # only one function in this example, but you can have multiple
        function_name = responseMessage["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(responseMessage["function_call"]["arguments"])
        if function_name == "request":
            function_response = fuction_to_call(
            classify=function_args.get("classify"),
        )
        if function_name == "question":
            function_response = fuction_to_call(
            userQuestion=function_args.get("userQuestion"),
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
        if function_name == "offer":
            function_response = fuction_to_call(
            text=function_args.get("text"),
        )
        print("response message", responseMessage)
        # Step 4: send the info on the function call and function response to GPT

        messagesForSecondCall = message.copy()
        messagesForSecondCall.append(responseMessage)  # extend conversation with assistant's reply
        messagesForSecondCall.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response

        secondResponse = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messagesForSecondCall,
        )  # get a new response from GPT where it can see the function response
        secondResponse = {"usage": secondResponse["usage"]["total_tokens"], "message": secondResponse["choices"][0]["message"]} 
        return {"firstResponse": firstResponse, "secondResponse": secondResponse}
    else: 
        return firstResponse


def updateSummaryGPT(summary, newText):
    messages = [{
        "role": "system",
        "content": f"""You are given a current summary of a conversation and a new message,
        you need to update the summary with the information in the last message. Make nice short simple sentences. Describe what happened in the conversation. Always include the previous actions from current summary.

        Summary: {summary}

        New message: {newText}"""
    }]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    
    responseMessage = response["choices"][0]["message"]['content']
    return responseMessage

def updatePersonalityGPT(personality, newText):
    messages = [{
        "role": "system",
        "content": f"""You are given a current user personality traits and a new message,
            you need to update the user personality with the information in the last message. Only add personality traits that reffer to character and nothing else. Make it small and consice. Print character traits in a list.

            User personality: {personality}

            New message: {newText}
            Updated personality:"""
    }]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    response_message = response["choices"][0]["message"]['content']
   
    return response_message