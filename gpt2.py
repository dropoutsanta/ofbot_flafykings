import openai
import openai
import json

# Ensure that you've set your OpenAI API key
openai.api_key = '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'

def callGPT(messages):
    print("Running")
    result = run_conversation(messages)
    return result

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def request(classify):
     """Get the current weather in a given location"""
     result = {
     "request": classify
     }
     print("REQUEST")
     print(classify)

     return json.dumps(result)
      

def question(userQuestion, assistantQuestion):
     """Get the current weather in a given location"""
     result = {
     "userQuestion": userQuestion,
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

def run_conversation(messages):
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "Send a picture"}]
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
                    }
                },
                "required": ["classify"],
            },
        },
        {
            "name": "question",
            "description": "Every time the user asks you a question you call this function",
            "parameters": {
                "type": "object",
                "properties": {
                    "userQuestion": {
                        "type": "string",
                        "description": "The answer to the question the user asked you",
                    },
                    "assistantQuestion": {
                        "type": "string",
                        "description": "The question you want to ask the user. After you responded to the user. You are also curious",
                    }
                },
                "required": ["userQuestion", "assistantQuestion" ],
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

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    
    response_message = response["choices"][0]["message"]
    print(response_message)
    
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
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
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_name)
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
        return json.loads(function_response)

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
        return json.dumps(response_message)


