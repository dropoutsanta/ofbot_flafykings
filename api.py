from flask import Flask, request
from telegram import Bot, Update
from setupBot import setup_bot



app = Flask(__name__)
bots = {}

@app.route('/add_bot', methods=['POST'])
def add_bot():
    print("RUNNNNNNNNING")
    return 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)