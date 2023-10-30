from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import logging
import asyncio

from utils import config_manager, chat_manager, model_manager

# Load the base context
base_context = config_manager.load_base_context()

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    try:
        chat_manager.ensure_chat_file_exists(user_id)
        logging.info(f"User {user_id} started the bot.")
        await update.message.reply_text('Welcome to the Llama Chatbot! Type your message.')
    except Exception as e:
        logging.error(f"Error starting chat for user {user_id}: {e}")

async def chat(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_id = update.message.from_user.id

    try:
        convo = chat_manager.load_chat(user_id)
        
        # Add the latest message to the conversation
        convo.append({"user": user_input})

        # Use the model to get a response
        response = model_manager.get_model_response(base_context, user_input)
        
        # Add model's response to conversation and save to file
        convo.append({"bot": response})
        chat_manager.save_chat(user_id, convo)
        
        logging.info(f"User {user_id} said '{user_input}', Bot replied with '{response}'.")
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error processing chat for user {user_id} with input '{user_input}': {e}")

def main() -> None:
    # Set up logging
    config_manager.setup_logging()

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