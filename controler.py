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
def request(stage):
     """Get the current weather in a given location"""
     result = {
     "request": stage
     }
     print("REQUEST")
     print(stage)

     return json.dumps(result)

def unknown(text):
     """Get the current weather in a given location"""
     result = {
     "unknown": text
     }
     print("UNKNOWN")
     return json.dumps(result)

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content": "Send a picture"}]
    system_msg = [{
                "role": "system",
                "content": """Given this conversation select the stage that best describe the state of the conversation. If empty that means it s the start
Conversation:"""}]
    functions = [
        {
            "name": "classify",
            "description": "Use to select the stage of the conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string",
                        "description": """Classify the stage of the conversation by selecting one of the follwoing id.
1: Start of conversation
2: Sending selfies
3: Sending sexy pictures of me dressed
4: Sending a nude picture of me
5: Sending a video of me masturbating
6: Sending a video of me fucking""",
                    }
                },
                "required": ["stage"],
            },
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=system_msg,
        functions=functions,
        function_call={"name": 'classify'}  
    )
    
    response_message = response["choices"][0]["message"]
    print(response_message)
    
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "classify": request,
           
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_name)
        if function_name == "classify":
            function_response = fuction_to_call(
            stage=function_args.get("stage"),
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


print(run_conversation())