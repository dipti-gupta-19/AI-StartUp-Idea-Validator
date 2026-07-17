from datetime import datetime, timedelta, timezone
from jose import  jwt , JWTError

import os
from . import schema



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data:dict):
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set")
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))  
        
        if uid is None:
            raise credentials_exception
        token_data = schema.TokenData(usid = uid)
        return token_data
    except JWTError:
        raise credentials_exception
   