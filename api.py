from flask import Flask, request
from telegram import Bot, Update
from app2 import setup_bot
import app2
import jsonify

app = Flask(__name__)
bots = {}

@app.route('/add_bot', methods=['POST'])
def add_bot():
    print("RUNNNNNNNNING")
    bot_data = request.json
    return jsonify({"message": "Bot added successfully"}), 200
    print(bot_data)
    if bot_data:
        bot_id = bot['id']
        updater = setup_bot(bot_data)
        app2.updaters.append(updater)

    return jsonify({"message": "Bot added successfully"}), 200
   

        # Here you could add the logic to restart or update your service as necessary

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)