import os
import json
import logging

def get_chat_filename(user_id):
    return f"chat_records/user_{user_id}.json"

def ensure_chat_file_exists(user_id):
    filename = get_chat_filename(user_id)
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)

def load_chat(user_id):
    ensure_chat_file_exists(user_id)
    filename = get_chat_filename(user_id)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chat(user_id, convo):
    filename = get_chat_filename(user_id)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convo, f, ensure_ascii=False)
