from flask import Flask, request, jsonify
from telegram import Bot, Update
from app2 import setup_bot, add_updater
import app2
from createEmbeddings import uploadImagesToVDB
from createDocumentEmbed import createDocEmbed

app = Flask(__name__)
bots = {}

@app.route('/add_bot', methods=['POST'])
def add_bot():
    print("RUNNNNNNNNING")
    bot_data = request.json
    
    if bot_data:
        updater = setup_bot(bot_data)
        add_updater(updater)
        return jsonify({"message": "Bot added successfully"}), 200
    else:
        return jsonify({"message": "Bot not added successfully"}), 200
   

        # Here you could add the logic to restart or update your service as necessary



@app.route('/modify_image', methods=['POST'])
def modify_image():
    
    print("RUNNNNNNNNING")
    bot_data = request.json
    id = bot_data['id']
    result = uploadImagesToVDB(id)

    if result == "Done":
        return jsonify({"message": "Bot added successfully"}), 200
    else:
        return jsonify({"message": "Bot not added successfully"}), 200
   

@app.route('/modify_bio', methods=['POST'])
def modify_bio():
    
    print("RUNNNNNNNNING")
    bot_data = request.json
    id = bot_data['id']
    result = createDocEmbed(id)

    if result == "Done":
        return jsonify({"message": "Bot added successfully"}), 200
    else:
        return jsonify({"message": "Bot not added successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)