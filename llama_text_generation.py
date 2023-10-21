from llama_cpp import Llama

def chat_with_llama():
    # Initialize the Llama model
    llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

    print("Welcome to the Llama Chatbot! (type 'exit' to quit)")
    
    while True:
        # Get user input
        user_input = input("You: ")

        # Check if the user wants to exit
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        # Use the model to generate a response directly without "Q:" and "A:"
        output = llm(user_input, max_tokens=32, echo=True)
        
        # Extract the response text from the model's output
        response = output['choices'][0]['text']
        
        print(f"Llama: {response}")

# Start the chatbot
chat_with_llama()

# {
#   "id": "cmpl-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#   "object": "text_completion",
#   "created": 1679561337,
#   "model": "./models/7B/llama-model.gguf",p
#   "choices": [
#     {
#       "text": "Q: Name the planets in the solar system? A: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto.",
#       "index": 0,
#       "logprobs": None,
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 14,
#     "completion_tokens": 28,
#     "total_tokens": 42
#   }
# }