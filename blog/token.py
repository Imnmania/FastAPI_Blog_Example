from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt



SECRET_KEY = '6a337fc2ab1b5c997ab880bdae179e8bbd9ae293fb2320a75975df6266d74bf6'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

