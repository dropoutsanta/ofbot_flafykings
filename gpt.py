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
def sendPicture(text):
     """Get the current weather in a given location"""
     result = {
     "text": text
     }
     print("SENDING PICTURE")
     print(text)

     return json.dumps(result)

def sendVideo(text):
     """Get the current weather in a given location"""
     result = {
     "video": text
     }
     print("SENDING VIDEO")
     

     return json.dumps(result)

def sendVideoFucking(text):
     """Get the current weather in a given location"""
     result = {
     "fuckingVideo": text
     }
     print("SENDING FUCKING VIDEO")
     

     return json.dumps(result)


def run_conversation(messages):
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "Send a picture"}]
    functions = [
        {
            "name": "send_picture",
            "description": "Sends back a picture of myself",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to go with the picture add sexy emojies",
                    }
                },
                "required": ["text"],
            },
        },
        {
            "name": "send_video",
            "description": "Sends back a video of me masturabating myself",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to go with the video add sexy emojies that reflects the video",
                    }
                },
                "required": ["text"],
            },
        },
        {
            "name": "send_video_fucking",
            "description": "Sends back a video of me getting fucked by a stranger",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to go with the video add sexy emojies that reflects the video",
                    }
                },
                "required": ["text"],
            },
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    
    response_message = response["choices"][0]["message"]
    
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "send_picture": sendPicture,
            "send_video": sendVideo,
            "send_video_fucking": sendVideoFucking,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            text=function_args.get("text"),
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


