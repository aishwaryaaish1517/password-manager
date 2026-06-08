# FILE: manager.py
# PURPOSE: All password operations — save, load, get, delete.
#          This is the "database" layer of our project.
#          The GUI buttons in main.py call these functions.

# 'json' is a built-in Python module.
# JSON (JavaScript Object Notation) lets us convert a Python
# dictionary into a saveable text string, and back again.
#
# Python dict  →  JSON string (to save)
# {"gmail": "pass1", "netflix": "pass2"}
# → '{"gmail": "pass1", "netflix": "pass2"}'
#
# JSON string  →  Python dict (to load back)
# '{"gmail": "pass1"}' → {"gmail": "pass1"}
import json

# 'os' to check if files exist on disk
import os

# Import our encrypt and decrypt functions from crypto_utils.py
from crypto_utils import encrypt_data, decrypt_data

# Constant: the filename for our encrypted passwords file.
# Using a constant means if we ever rename this file,
# we only change it in ONE place — right here.
PASSWORDS_FILE = "passwords.enc"


def load_passwords() -> dict:
    """
    Reads the encrypted file and returns all passwords
    as a plain Python dictionary.

    Steps:
      1. If file doesn't exist → return empty dict {}
      2. Read raw encrypted bytes from file
      3. Decrypt bytes → JSON string
      4. Parse JSON string → Python dictionary
      5. Return the dictionary

    Returns:
        dict: e.g. {"gmail": "pass1", "netflix": "pass2"}
    """

    # If the file doesn't exist (first run), return empty dict
    if not os.path.exists(PASSWORDS_FILE):
        return {}

    # Open file in read-binary mode to get encrypted bytes
    with open(PASSWORDS_FILE, "rb") as f:
        encrypted_content = f.read()

    # If the file is empty for some reason, return empty dict
    if not encrypted_content:
        return {}

    # Decrypt the bytes back into a JSON string
    decrypted_json = decrypt_data(encrypted_content)

    # json.loads() = "load from string"
    # Converts JSON string → Python dictionary
    return json.loads(decrypted_json)


def save_passwords(passwords: dict):
    """
    Takes the passwords dictionary, encrypts it, and writes
    it to the passwords.enc file.

    Steps:
      1. Convert Python dict → JSON string
      2. Encrypt JSON string → encrypted bytes
      3. Write encrypted bytes to file (overwrites old content)

    Args:
        passwords (dict): All passwords to save.
    """

    # json.dumps() = "dump to string"
    # Converts Python dictionary → JSON-formatted string
    # indent=4 makes it nicely formatted (4 spaces per level)
    json_string = json.dumps(passwords, indent=4)

    # Encrypt the JSON string → encrypted bytes
    encrypted_content = encrypt_data(json_string)

    # Write the encrypted bytes to file
    # "wb" = write binary (overwrites previous content entirely)
    with open(PASSWORDS_FILE, "wb") as f:
        f.write(encrypted_content)


def add_password(service: str, username: str, password: str) -> bool:
    """
    Adds or updates a password entry.

    Args:
        service  (str): Service name, e.g. "gmail"
        username (str): Username/email for that service
        password (str): The actual password

    Returns:
        bool: True if this is a NEW entry, False if we updated existing
    """

    # Load existing passwords so we don't overwrite them
    passwords = load_passwords()

    # Check if this service already exists (for the return value)
    is_new = service not in passwords

    # Store as a nested dictionary:
    # {"gmail": {"username": "user@gmail.com", "password": "abc123"}}
    # WHY nested? So we can store BOTH username AND password per service.
    passwords[service] = {
        "username": username,
        "password": password
    }

    # Save the updated dictionary back to the encrypted file
    save_passwords(passwords)

    return is_new  # Tell the caller if it was new or updated


def get_password(service: str) -> dict:
    """
    Retrieves the username and password for a specific service.

    Args:
        service (str): The service name to look up

    Returns:
        dict: {"username": "...", "password": "..."} or None if not found
    """

    passwords = load_passwords()

    # dict.get(key) returns the value if key exists, else None
    # So if "gmail" exists: returns {"username": ..., "password": ...}
    # If "gmail" doesn't exist: returns None
    return passwords.get(service)


def get_all_services() -> list:
    """
    Returns a list of all saved service names.
    Used by the GUI to populate the password table.

    Returns:
        list: e.g. ["gmail", "netflix", "instagram"]
    """

    passwords = load_passwords()

    # .keys() returns all dictionary keys (the service names)
    # list() converts the dict_keys object into a plain list
    return list(passwords.keys())


def delete_password(service: str) -> bool:
    """
    Deletes the password entry for a specific service.

    Args:
        service (str): The service name to delete

    Returns:
        bool: True if deleted successfully, False if not found
    """

    passwords = load_passwords()

    # Check if service exists before trying to delete
    if service not in passwords:
        return False  # Not found — nothing to delete

    # del dict[key] removes that key-value pair from the dictionary
    del passwords[service]

    # Save the updated (now smaller) dictionary back to file
    save_passwords(passwords)

    return True  # Successfully deleted


def get_all_passwords_data() -> dict:
    """
    Returns the complete passwords dictionary.
    Used by the GUI table to show all entries at once.

    Returns:
        dict: Full passwords dict with usernames and passwords
    """
    return load_passwords()
