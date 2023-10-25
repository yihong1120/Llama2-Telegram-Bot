from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from llama_cpp import Llama
import asyncio

# Initialize the Llama model
llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Llama Chatbot! Type your message.')

def chat(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text

    # Set a prompt for the model if you want
    prompt = f"Q: {user_input} A: "

    # Use the model to generate a response
    output = llm(prompt, max_tokens=32, echo=True)
    
    # Extract the response text from the model's output
    response = output['choices'][0]['text'].replace(prompt, "").strip()

    update.message.reply_text(response)

def main() -> None:
    # Set your telegram token here
    TOKEN = ""
    bot = Bot(token=TOKEN)
    app = Application.builder().token(TOKEN).build()

    text_filter = (filters.TEXT & ~filters.COMMAND)  # 修改了這一行
    app.add_handler(MessageHandler(text_filter, chat))

    app.run_polling()

if __name__ == '__main__':
    main()