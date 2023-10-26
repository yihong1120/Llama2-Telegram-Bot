import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from llama_cpp import Llama
import asyncio
import os

# Initialize the Llama model
llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

# Load the base context from an external file
with open("config/francine_context.txt", "r", encoding="utf-8") as file:
    base_context = file.read().strip()

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    filename = f"user_{user_id}.json"
    
    # Check if file exists, if not create it with an empty list
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    
    await update.message.reply_text('Welcome to the Llama Chatbot! Type your message.')

async def chat(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_id = update.message.from_user.id
    filename = f"user_{user_id}.json"

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
    # prompt = base_context + f"\n\nQ: {user_input} A: "
    prompt = base_context + f"\n\nUser said: {user_input}"

    # Use the model to generate a response
    output = llm(prompt, max_tokens=150, echo=True)
    
    # Extract the response text from the model's output
    response = output['choices'][0]['text'].replace(prompt, "").strip()

    # Add model's response to conversation and save to file
    convo.append({"bot": response})
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convo, f, ensure_ascii=False)
    
    await update.message.reply_text(response)

def main() -> None:
    # Set your telegram token here
    TOKEN = "6821220940:AAHZGou5OSZpWJiBeXOPzCOHH39BT2T4imc"
    bot = Bot(token=TOKEN)
    app = Application.builder().token(TOKEN).build()

    text_filter = (filters.TEXT & ~filters.COMMAND)
    app.add_handler(MessageHandler(text_filter, chat))

    app.run_polling()

if __name__ == '__main__':
    main()