import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_message(message, key):
    if not isinstance(message, str):
        message = str(message)

    key = key.encode('utf-8')
    key = pad(key, AES.block_size)[:32]  # Ensure key is 32 bytes
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return base64.b64encode(encrypted_message).decode('utf-8')


def decrypt_message(encrypted_message, key):
    try:
        key = key.encode('utf-8')
        key = pad(key, AES.block_size)[:32]  # Ensure key is 32 bytes
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_message = base64.b64decode(encrypted_message)
        decrypted_message = cipher.decrypt(encrypted_message)
        unpadded_message = unpad(decrypted_message, AES.block_size)
        return unpadded_message.decode('utf-8')
    except Exception as e:
        return f"Erreur de déchiffrement: {str(e)}"
