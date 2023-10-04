from flask import Flask, request, jsonify
from handlers.pineconeHandler import upsertPDFDocument
from setupFunctions import setupBot

app = Flask(__name__)
bots = {}

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
    updaters = []
    bot_data = request.json
    
    if bot_data:
        updater = setupBot(bot_data)
        updaters.append(updater)
        return jsonify({"message": "Bot added successfully"}), 200
    else:
        return jsonify({"message": "Bot not added successfully"}), 200
   

        # Here you could add the logic to restart or update your service as necessary


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