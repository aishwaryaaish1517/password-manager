# FILE: crypto_utils.py
# PURPOSE: Handles ALL encryption and decryption.
#          This file is the "lock and key" of our project.
#          The GUI (main.py) calls these functions when
#          saving or loading passwords.

# 'os' is a built-in Python module (no install needed).
# We use os.path.exists() to check if a file already exists.
import os

# 'Fernet' is from the 'cryptography' library we installed.
# Fernet = symmetric encryption (same key locks AND unlocks).
# It uses AES-128-CBC + HMAC-SHA256 under the hood.
# AES-128 is the same encryption used by banks and governments.
from cryptography.fernet import Fernet


def generate_key():
    """
    Creates a brand-new random encryption key and saves it
    to a file called 'secret.key'.

    This function is called ONLY ONCE — the very first time
    the program runs. After that, we always reuse the same key.

    WHY save to a file?
    Because if the program closes and restarts, we need the
    same key to decrypt the saved passwords. Without it,
    all saved passwords are PERMANENTLY unreadable.
    """

    # Fernet.generate_key() creates a cryptographically secure
    # random 256-bit key, returned as base64-encoded bytes.
    key = Fernet.generate_key()

    # Open (or create) 'secret.key' in write-binary mode.
    # "wb" → w = write (overwrite if exists), b = binary
    # 'with' ensures the file is automatically closed after writing.
    with open("secret.key", "wb") as key_file:
        key_file.write(key)  # Write the raw key bytes to disk


def load_key():
    """
    Reads and returns the encryption key from 'secret.key'.

    Called every time we encrypt or decrypt something.

    Returns:
        bytes: The encryption key as raw bytes.
    """

    # If 'secret.key' doesn't exist yet (first ever run)...
    if not os.path.exists("secret.key"):
        generate_key()  # ...create one automatically

    # Open 'secret.key' in read-binary mode.
    # "rb" → r = read, b = binary
    with open("secret.key", "rb") as key_file:
        return key_file.read()  # Return all bytes from the file


def encrypt_data(data: str) -> bytes:
    """
    Converts a plain text string into encrypted (unreadable) bytes.

    Example:
        Input  → "MyPassword123"
        Output → b'gAAAAABl7x...' (random-looking gibberish)

    Args:
        data (str): The plain text string to encrypt.

    Returns:
        bytes: The encrypted data (unreadable without the key).
    """

    key = load_key()       # Get our encryption key from file
    f = Fernet(key)        # Create a Fernet cipher using that key

    # .encode() converts string → bytes  ("hello" → b"hello")
    # Fernet only works with bytes, not strings, so we encode first.
    # f.encrypt() then scrambles those bytes using our key.
    return f.encrypt(data.encode())


def decrypt_data(encrypted_data: bytes) -> str:
    """
    Converts encrypted bytes back into readable plain text.

    Example:
        Input  → b'gAAAAABl7x...' (gibberish bytes)
        Output → "MyPassword123" (original text)

    Args:
        encrypted_data (bytes): The encrypted bytes to decode.

    Returns:
        str: The original plain text string.
    """

    key = load_key()       # Get the same key used to encrypt
    f = Fernet(key)        # Create Fernet cipher with that key

    # f.decrypt() unscrambles bytes back to original bytes
    # .decode() converts bytes → string  (b"hello" → "hello")
    return f.decrypt(encrypted_data).decode()