from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(pasword : str):
    return pwd_context.hash(pasword)

def verify(plain_password , hashed_password):
    print(type(pwd_context.verify(plain_password, hashed_password)))
    return pwd_context.verify(plain_password, hashed_password)
    