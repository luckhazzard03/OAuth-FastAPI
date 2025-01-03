# src/utils/hash.py

import bcrypt

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")  # Verificación adicional
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica si la contraseña en texto plano coincide con el hash
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
