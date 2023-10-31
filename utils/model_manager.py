from llama_cpp import Llama

# Instantiate the Llama model with the given model path
llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

def get_model_response(base_context: str, user_input: str, max_tokens: int = 150) -> str:
    """
    Get the response from the model for a given user input.

    This function generates a prompt by appending the user input to the base context, 
    and then feeds this prompt to the model. The model's response is then extracted, 
    cleaned, and returned.

    Args:
        base_context (str): The base context to be used for generating the prompt.
        user_input (str): The user's input.
        max_tokens (int, optional): The maximum number of tokens to be generated by the model. Defaults to 150.

    Returns:
        str: The model's response.
    """
    # Generate the prompt
    prompt = base_context + f"\n\nQ: {user_input} A: "
    
    # Feed the prompt to the model and get the output
    output = llm(prompt, max_tokens=max_tokens, echo=True)
    
    # Extract, clean, and return the model's response
    return output['choices'][0]['text'].replace(prompt, "").strip()
