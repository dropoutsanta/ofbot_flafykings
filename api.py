from flask import Flask, request, jsonify
from telegram import Bot, Update
from app2 import setup_bot
import app2


app = Flask(__name__)
bots = {}

@app.route('/add_bot', methods=['POST'])
def add_bot():
    print("RUNNNNNNNNING")
    return jsonify({"message": "Bot added successfully"}), 200

        # Here you could add the logic to restart or update your service as necessary

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)