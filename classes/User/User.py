import json

class User:
    def __init__(self, id, username, firstName, lastName, languageCode, botId):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.languageCode = languageCode
        self.botId = botId
    