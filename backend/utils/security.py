from cryptography.fernet import Fernet
import os

# Load or generate encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()  # Generate a key if missing
    print(f"Generated Encryption Key: {ENCRYPTION_KEY}")  # Save this key securely!

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    """Encrypts sensitive data."""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts sensitive data."""
    return fernet.decrypt(encrypted_data.encode()).decode()
