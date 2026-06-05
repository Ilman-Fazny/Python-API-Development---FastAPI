import bcrypt

def hash_password(password: str) -> str:
    # Hash a password using bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify a password against its hash using bcrypt
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # Return False if the password in the database is not a valid bcrypt hash (e.g. legacy plain text)
        return False