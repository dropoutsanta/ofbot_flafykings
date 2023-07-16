from flask import Flask, request
from telegram import Bot, Update
from app2 import setup_bot
import app2


app = Flask(__name__)
bots = {}

@app.route('/add_bot', methods=['POST'])
def add_bot():
    print("RUNNNNNNNNING")
    return 
    bot_token = request.json.get('bot_token')
    if bot_token:
        bot_id = bot['id']
        updater = setup_bot(bot)
        app2.updaters.append(updater)
    if bot_token:
        bot = Bot(token=bot_token)
        dispatcher = Dispatcher(bot, None, workers=0)
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
        bots[bot_token] = {'bot': bot, 'dispatcher': dispatcher}

        # Here you could add the logic to restart or update your service as necessary

        return 'Bot added successfully', 200
    else:
        return 'No bot token provided', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)