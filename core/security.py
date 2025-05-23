import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from cryptography.fernet import Fernet

# Get environment variables safely
SECRET_KEY = os.getenv("SECRETY_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
FERNET_KEY = os.getenv("SECOND_S_KEY")

if not SECRET_KEY or not FERNET_KEY:
    raise RuntimeError("SECRET_KEY and SECOND_S_KEY must be set in environment variables.")

secondCryp = Fernet(FERNET_KEY.encode())

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        # Decrypt first
        decrypted_token = secondCryp.decrypt(token.encode()).decode()
        payload = jwt.decode(decrypted_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except (JWTError, Exception):
        raise credentials_exception

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encrypted_token = secondCryp.encrypt(jwt_token.encode())
    return encrypted_token.decode()

def decode_token(encrypted_token: str):
    try:
        decrypted_jwt = secondCryp.decrypt(encrypted_token.encode()).decode()
        payload = jwt.decode(decrypted_jwt, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
