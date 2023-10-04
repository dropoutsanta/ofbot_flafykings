from flask import Flask, request, jsonify
from handlers.pineconeHandler import upsertPDFDocument
from handlers.supabaseHandler import getBot, postBot, updateAutobiography, updateSystemMessage
from setupFunctions import setupBot

app = Flask(__name__)
updaters = []
# @app.route('/add-bot', methods=['POST'])
# @app.route('/delete-bot', methods=['POST'])
# @app.route('/update-bot', methods=['POST'])

# @app.route('/add-media', methods=['POST'])
# @app.route('/delete-media', methods=['POST'])
# @app.route('/update-media', methods=['POST'])

# @app.route('/add-document', methods=['POST'])
# @app.route('/delete-document', methods=['POST'])
# @app.route('/update-document', methods=['POST'])


@app.route('/add_bot', methods=['POST'])
def add_bot():
    if request.json:
        telegramAPIKey = request.json['telegram_API_key']
        systemMessage = request.json['system_message']
        biography = request.json['autobiography']
        bot = postBot(telegramAPIKey, systemMessage, biography).data[0]

        updater = setupBot(bot)
        updaters.append(updater)
        return jsonify({"message": "Bot added successfully"}), 200
    else:
        return jsonify({"message": "Bot not added successfully"}), 200
   

        # Here you could add the logic to restart or update your service as necessary

@app.route('/update_system_message', methods=['PATCH'])
def update_system_message():
    if request.json:
        id = request.json['id']
        systemMessage = request.json['system_message']

        updateSystemMessage(id, systemMessage)

        return jsonify({"message": "System message was updated successfully"}), 200
    else:
        return jsonify({"message": "System message was not updated successfully"}), 200

@app.route('/update_autobiography', methods=['PATCH'])
def update_autobiography():
    if request.json:
        id = request.json['id']
        biography = request.json['autobiography']

        updateAutobiography(id, biography)

        return jsonify({"message": "Autobiography was updated successfully"}), 200
    else:
        return jsonify({"message": "Autobiography was not updated successfully"}), 200


# @app.route('/modify_image', methods=['POST'])
# def modify_image():
#     bot_data = request.json
#     id = bot_data['id']
#     result = uploadImagesToVDB(id)

#     if result == "Done":
#         return jsonify({"message": "Bot added successfully"}), 200
#     else:
#         return jsonify({"message": "Bot not added successfully"}), 200
   

@app.route('/add-document', methods=['POST', 'GET'])
def addDocument():
    document = request.files['document']
    botId = request.args.get('id')
    upsertPDFDocument(botId, document)
    return jsonify({"message": "Document was added"}), 200