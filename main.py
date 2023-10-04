from handlers.supabaseHandler import getAllBots, getBot
from setupFunctions import setupBot

updaters = []

if __name__ == "__main__":
    # Fetch all the API keys and system messages
    bots = getBot(1)

    # Setup a bot for each token
    for bot in bots:
        updater = setupBot(bot)
        updaters.append(updater)


