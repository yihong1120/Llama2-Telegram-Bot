from llama_cpp import Llama

llm = Llama(model_path="./llama-2-7b.Q4_K_M.gguf")

def get_model_response(base_context, user_input, max_tokens=150):
    prompt = base_context + f"\n\nQ: {user_input} A: "
    output = llm(prompt, max_tokens=max_tokens, echo=True)
    return output['choices'][0]['text'].replace(prompt, "").strip()
