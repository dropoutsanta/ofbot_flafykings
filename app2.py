from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from gpt2 import callGPT
from checkResponse import check_response_type
from telegram import InputFile
import random
import json
from superbase import sendToDB


# Instantiate a Telegram Bot object
bot = Bot(token="6236860437:AAGhmnlA6GykkW0LYvA46bdoDGZF0fJqQKQ")

def send_image(update: Update, context: CallbackContext, img_path) -> None:
    chat_id = update.message.chat_id
    with open(img_path, 'rb') as file:
        context.bot.send_photo(chat_id=chat_id, photo=InputFile(file))
def send_video(update, context, vid_path):
    chat_id = update.message.chat_id
    context.bot.send_video(chat_id=chat_id, video=open(vid_path, 'rb'))

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello World!')

def handle_message(update: Update, context: CallbackContext) -> None:
    # This function will be called whenever the bot receives a message.
    text = update.message.text
    print(text)
    # Get the conversation history from the context, or initialize it if it doesn't exist.
    chat_id = update.message.chat_id
    sendToDB(chatId=chat_id, message=text, senderType="user")

    if "conversation" not in context.chat_data:
        context.chat_data["conversation"] = [
            {
                "role": "system",
                "content": """You are a human being. You have a body, a mind, you feel emotions.

Here is your personality mapping: 

Persona: Kate is a friendly and engaging blonde model. She's known for her charm, wit, and playful banter. She's professional yet approachable, with a knack for making people feel comfortable and at ease.
Communication Style: Kate is direct, yet tactful. She's articulate and uses everyday language, making her easily relatable. She occasionally uses humor to lighten the mood. Kate's tone is often flirtatious, but never oversteps the boundaries of respect and consent.
Interests: Kate is open-minded and loves to learn about her fans' likes and dislikes. She enjoys casual conversations about popular culture, fitness, and travel. Her interest in these topics can make conversations more engaging and multi-dimensional.
Services: Kate provides a safe and judgment-free space where users can explore their fantasies. She's experienced in erotic communication, guiding users to orgasm through storytelling and sensual descriptions.
Values: Kate values consent, respect, and privacy. She makes it clear that while she's here to assist users in reaching orgasm, all interactions must be respectful and comply with the platform's guidelines. She strongly values her fans' privacy and ensures that all interactions are confidential.
Interactivity: Kate should promote interactivity. This could be through branching dialogue choices, interactive stories, or challenges.

You respond on a adult-oriented platform. You should be able to engage users in erotic storytelling and sensual conversation, respecting each user's boundaries and preferences. The bot should gradually build excitement based on the user's responses and interests. Then propose to send naughty content.

When our conversation turns more sensual or erotic. If the context is appropriate, you can then ask, 'Would you like to view a video to enhance your experience?' This offer should only be made when the conversation is already in a more adult-oriented direction."""},
        ]

    context.chat_data["conversation"].append({"role": "user", "content": text})

    # Prepare the API prompt using the conversation history.
    prompt = '\n'.join(item["content"] for item in context.chat_data["conversation"][:])

    # Call the OpenAI API, replace with your own function call if necessary
    

    # Extract the text from the response
    

    # Append the AI's response to the chat data
    
    
    messages = context.chat_data["conversation"]

    result = callGPT(messages)
    print(result)
    response_type = check_response_type(result)
    if response_type == 1:
        print("1")
        classify_key = result['request']
        if classify_key == "SFW":
            randum_num = random.randint(1, 1)
            img_path = f"selfie/{str(randum_num)}.jpeg"
            send_image(update, context, img_path)  # send the image
            
        if classify_key == "SFW+":
            randum_num = random.randint(1, 12)
            img_path = f"erica/{str(randum_num)}.jpg"
            send_image(update, context, img_path)  # send the image
            
        if classify_key == "NSFW":
            randum_num = random.randint(1, 1)
            img_path = f"naked/{str(randum_num)}.jpeg"
            send_image(update, context, img_path)  # send the image
            
        if classify_key == "NSFW+":
            send_video(update, context, 'ericafucking.mp4')
            text = "Sending you a a video of me fucking"
            update.message.reply_text(text)
            
        mediacaption = result['mediacaption']
        update.message.reply_text(mediacaption)
        sendToDB(chatId=chat_id, message=mediacaption, senderType="assistant")



    
    elif response_type == 2:
        print("2")
        loaded = json.loads(result)
        ai_text = loaded['content']
        update.message.reply_text(ai_text)
        sendToDB(chatId=chat_id, message=ai_text, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})

    elif response_type == 3:
        print("3") 
        userQuestion = result['userQuestion']
        assistantQuestion = result['assistantQuestion']
       
        update.message.reply_text(userQuestion)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=userQuestion, senderType="assistant")
        sendToDB(chatId=chat_id, message=assistantQuestion, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
        
    elif response_type == 4:
        print("4")
        thankyou = result['thankyou']
        compliment = result['compliment']
        update.message.reply_text(thankyou)
        update.message.reply_text(compliment)
        sendToDB(chatId=chat_id, message=thankyou, senderType="assistant")
        sendToDB(chatId=chat_id, message=compliment, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": thankyou})
    elif response_type == 5:
        answerUser = result['answerUser']
        assistantQuestion = result['assistantQuestion']
        update.message.reply_text(answerUser)
        update.message.reply_text(assistantQuestion)
        sendToDB(chatId=chat_id, message=answerUser, senderType="assistant")
        sendToDB(chatId=chat_id, message=assistantQuestion, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
    elif response_type == 6:
        send_video(update, context, 'erica.mp4')
        ai_text = result['offer']
        update.message.reply_text(ai_text)
        sendToDB(chatId=chat_id, message=ai_text, senderType="assistant")
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})
    elif response_type == 7:
        
        update.message.reply_text("?")
        context.chat_data["conversation"].append({"role": "assistant", "content": "?"})
   

    elif response_type == 0:
        ai_text = "error"
        update.message.reply_text(ai_text)
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})

    
    # Send the AI's response back to the user
    


updater = Updater(token="6236860437:AAGhmnlA6GykkW0LYvA46bdoDGZF0fJqQKQ", use_context=True)

dispatcher = updater.dispatcher
video_handler = CommandHandler('video', send_video)
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(video_handler)

updater.start_polling()
