from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oath_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret key
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#algorith
ALGORITHM = "HS256"
#expirationtime
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def Access_tokens(data : dict): #creating tokens 
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,  algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str, credential_exceptions): #as the name suggests this verifies the the that the payload matches the 

    try:
        payload = jwt.decode(token , SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exceptions
        
        token_Data = schemas.token_data(id=id)

    except JWTError:
        raise credential_exceptions

    return token_Data



def get_current_user(token: str = Depends(oath_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could Not Validate Credentials", headers={"WWW-authenticate": "Bearer"})

    return verify_access_token(token , credential_exception)
