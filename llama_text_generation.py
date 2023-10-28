import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from llama_cpp import Llama
import asyncio
import os
import logging
from datetime import datetime

# Initialize the Llama model
llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

# Load the base context from an external file
with open("config/prompt.txt", "r", encoding="utf-8") as file:
    base_context = file.read().strip()

def setup_logging():
    """ Set up logging with a new file for each day. """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, datetime.now().strftime('%Y%m%d.log')),
                        level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a new handler to also print logs to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

setup_logging()

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    filename = f"chat_records/user_{user_id}.json"
    
    try:
        # Check if file exists, if not create it with an empty list
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump([], f)
        
        logging.info(f"User {user_id} started the bot.")
        await update.message.reply_text('Welcome to the Llama Chatbot! Type your message.')
    except Exception as e:
        logging.error(f"Error starting chat for user {user_id}: {e}")

async def chat(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_id = update.message.from_user.id
    filename = f"chat_records/user_{user_id}.json"

    try:
        # Ensure the file exists, if not, create it with an empty list
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
        
        # Load previous conversations
        with open(filename, 'r', encoding='utf-8') as f:
            convo = json.load(f)
            
        # Add the latest message to the conversation
        convo.append({"user": user_input})

        # Prepare the full prompt for the model
        prompt = base_context + f"\n\nQ: {user_input} A: "

        # Use the model to generate a response
        output = llm(prompt, max_tokens=150, echo=True)
        
        # Extract the response text from the model's output
        response = output['choices'][0]['text'].replace(prompt, "").strip()

        # Add model's response to conversation and save to file
        convo.append({"bot": response})
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(convo, f, ensure_ascii=False)
        
        logging.info(f"User {user_id} said '{user_input}', Bot replied with '{response}'.")
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error processing chat for user {user_id} with input '{user_input}': {e}")

def main() -> None:
    # Ensure we're using a new log file if the day has changed
    setup_logging()

    # Set your telegram token here
    TOKEN = ""
    bot = Bot(token=TOKEN)
    app = Application.builder().token(TOKEN).build()

    text_filter = (filters.TEXT & ~filters.COMMAND)
    app.add_handler(MessageHandler(text_filter, chat))

    logging.info("Bot started and is now polling...")
    app.run_polling()

if __name__ == '__main__':
    main()