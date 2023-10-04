import requests
import json

from variables.apiKeys import SUPABASE_API_KEY

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
                "description": "Every time the user asks you a personal question that requires additional information",
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
            
        ]
    return functions

