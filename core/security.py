from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from cryptography.fernet import Fernet

import os

SECRET_KEY = os.getenv("SECRETY_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
FERNET_KEY = os.getenv("SECOND_S_KEY").encode()
secondCryp = Fernet(FERNET_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encrypted_token = secondCryp.encrypt(jwt_token.encode())
    return encrypted_token.decode() 
    #return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(encrypted_token: str):
    try:
        decrypted_jwt = secondCryp.decrypt(encrypted_token.encode()).decode()
        payload = jwt.decode(decrypted_jwt, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
