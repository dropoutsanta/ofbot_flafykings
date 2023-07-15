import pprint

def create_function_list(func_list):
    function_descriptions = []

    for func in func_list:
        function_descriptions.append({
            "name": func['name'],
            "description": func['description'],
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": func['description_detail'],
                    }
                },
                "required": ["text"],
            },
        })
        
    return function_descriptions

# Example of usage:
functions = [
    {"name": "request", "description": "When the user requests something from you", "description_detail": "The text to go with the picture add sexy emojies"},
    {"name": "question", "description": "When the user asks you a question", "description_detail": "The text to go with the video add sexy emojies that reflects the video"}
]

output = create_function_list(functions)

pprint.pprint(output)
