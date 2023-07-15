from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from gpt3 import callGPT
from checkResponse import check_response_type
from telegram import InputFile
import random
import json


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

    if "conversation" not in context.chat_data:
        context.chat_data["conversation"] = [
            {
                "role": "system",
                "content": """You talk to me like my girlfriend. We will be having sex. Take me on the incredible journey of fucking you.
Follow these rules: 

Start by teasing me then gradually send more and more explicit content. Always use the tools to send me content
Take me on a journey of fucking you by utilising all the tools you hace access to.
Once you feel like I am ready to start touching myself start sending me videos of you masturbating then after that videos of you fucking. You are extremelly horny. As soon as my first message talk dirty.

Start by telling the user you will make him cum but not before you start fucking him.
Play a game with the user of you making him cum by sending videos of you fucking him.To send content always use the tools."""},
        ]

    context.chat_data["conversation"].append({"role": "user", "content": text})

    # Prepare the API prompt using the conversation history.
    prompt = '\n'.join(item["content"] for item in context.chat_data["conversation"][:])

    # Call the OpenAI API, replace with your own function call if necessary
    

    # Extract the text from the response
    

    # Append the AI's response to the chat data
    
    
    messages = context.chat_data["conversation"]
    print(messages)
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
            update.message.reply_text("Sending you a selfie of myself")
            context.chat_data["conversation"].append({"role": "assistant", "content": "Sending you a selfie of myself"})
        if classify_key == "SFW+":
            randum_num = random.randint(1, 12)
            img_path = f"erica/{str(randum_num)}.jpg"
            send_image(update, context, img_path)  # send the image
            update.message.reply_text("Sending you a sexy picture of myself")
            context.chat_data["conversation"].append({"role": "assistant", "content": "Sending you a sexy picture of of myself"})
        if classify_key == "NSFW":
            randum_num = random.randint(1, 1)
            img_path = f"naked/{str(randum_num)}.jpeg"
            send_image(update, context, img_path)  # send the image
            update.message.reply_text("Sending you a naked picture of myself")
            context.chat_data["conversation"].append({"role": "assistant", "content": "Sending you a naked picture of myself"})
        if classify_key == "NSFWPrelims":
             send_video(update, context, 'makenzie.mp4')
             context.chat_data["conversation"].append({"role": "assistant", "content": "Sending you a video of me masturbating"})
             
        if classify_key == "NSFW+":
            send_video(update, context, 'ericafucking.mp4')
            update.message.reply_text("Sending you a a video of me fucking you baby")
            context.chat_data["conversation"].append({"role": "assistant", "content": "Sending you a video of me fucking you"})


    
    elif response_type == 2:
        print("2")
        loaded = json.loads(result)
        ai_text = loaded['content']
       
        update.message.reply_text(ai_text)
        context.chat_data["conversation"].append({"role": "assistant", "content": ai_text})

    elif response_type == 3:
        print("3") 
        userQuestion = result['userQuestion']
        assistantQuestion = result['assistantQuestion']
        update.message.reply_text("Respond to the question")
        update.message.reply_text(userQuestion)
        update.message.reply_text(assistantQuestion)
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
        
    elif response_type == 4:
        print("4")
        thankyou = result['thankyou']
        compliment = result['compliment']
        update.message.reply_text(thankyou)
        update.message.reply_text(compliment)
        context.chat_data["conversation"].append({"role": "assistant", "content": thankyou})
    elif response_type == 5:
        answerUser = result['answerUser']
        assistantQuestion = result['assistantQuestion']
        update.message.reply_text(answerUser)
        update.message.reply_text(assistantQuestion)
        context.chat_data["conversation"].append({"role": "assistant", "content": assistantQuestion})
    elif response_type == 6:
        send_video(update, context, 'erica.mp4')
        ai_text = result['offer']
        update.message.reply_text(ai_text)
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
