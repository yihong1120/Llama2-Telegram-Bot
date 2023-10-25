# Llama2-Telegram-Bot
Integration of the advanced llama2 AI model with Telegram to provide real-time chatbot responses. Seamless interaction, smart replies, and scalable deployment.

### Prerequisites

1. **Python**: You need to have Python installed on your system.
2. **Python Packages**: 
    - `telegram`
    - `json`
    - `os`
    - `asyncio`
3. **Llama C++ Library**: Ensure you've properly installed and set up the `llama_cpp` library. The provided code assumes you have the Llama model stored at `./llama-2-7b.Q4_K_M.gguf`.

### Setting Up

1. Clone this repository:
    ```bash
    git clone https://github.com/yihong1120/Llama2-Telegram-Bot.git
    cd Llama2-Telegram-Bot
    ```

2. Install necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Replace the `TOKEN` placeholder in the code with your Telegram bot token. This is essential for the bot to function.

### Usage

Run the script:
```bash
python llama_text_generation.py
```

Upon execution, the bot will start listening to incoming messages. Users can start a conversation with the bot on Telegram. The bot will then respond to user messages using the Llama model.

The chatbot keeps track of the last 20 messages per user to ensure it has a relevant context while generating responses. Conversations are saved as JSON files, named according to the user's ID.

### Contributing

Feel free to fork this repository and make modifications. Pull requests are welcome!