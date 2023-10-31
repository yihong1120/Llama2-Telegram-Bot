import os
import json
import logging
from typing import List, Any

def get_chat_filename(user_id: int) -> str:
    """
    Given a user ID, returns the filename where the chat records for that user are stored.

    Args:
        user_id (int): The ID of the user.
    
    Returns:
        str: The filename of the chat records for the given user.
    """
    # Use an f-string to create the filename. This is a concise and readable way to insert variables into strings.
    return f"chat_records/user_{user_id}.json"

def ensure_chat_file_exists(user_id: int) -> None:
    """
    Ensures that a chat record file exists for the given user. If it does not exist, a new one is created.

    Args:
        user_id (int): The ID of the user.
    """
    filename = get_chat_filename(user_id)
    # Use the os module to check if the file already exists.
    if not os.path.exists(filename):
        # If the file does not exist, create a new one and initialise it with an empty list.
        with open(filename, 'w') as f:
            json.dump([], f)

def load_chat(user_id: int) -> List[Any]:
    """
    Loads the chat records for the given user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Any]: The chat records for the given user.
    """
    ensure_chat_file_exists(user_id)
    filename = get_chat_filename(user_id)
    # Open the file in read mode and load the JSON data.
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_chat(user_id: int, convo: List[Any]) -> None:
    """
    Saves the given chat records for the given user.

    Args:
        user_id (int): The ID of the user.
        convo (List[Any]): The chat records to save.
    """
    filename = get_chat_filename(user_id)
    # Open the file in write mode and dump the JSON data.
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(convo, f, ensure_ascii=False)
