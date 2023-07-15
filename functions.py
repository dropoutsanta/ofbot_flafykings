functions = [
        {
            "name": "request",
            "description": "When the user requests something from you",
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
            "name": "question",
            "description": "When the user asks you a question",
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
            "name": "compliments",
            "description": "When the user compliments you",
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
            "name": "user_info",
            "description": "When the user provides information about himself",
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
            "name": "offer",
            "description": "when the user makes you an offer",
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
            "name": "unknown",
            "description": "When you don't understant the user input",
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


