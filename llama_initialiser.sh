#!/bin/bash

# Fetch the file using wget
wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf

# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Execute the Python script
python llama_text_generation.py
