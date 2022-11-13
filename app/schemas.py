from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseConfig
from typing import Optional

BaseConfig.arbitrary_types_allowed = True

class postbase(BaseModel):
    title: str
    content: str
    published: bool = False #default value to True

    class Config:
        orm_mode = True

class post(postbase):
    title: str
    content: str
    published: bool

    uselist=False


class postcreate(postbase):
    id: int

    class Config:
        orm_mode = True

class usercreate(BaseModel):
    email: EmailStr
    password: str

class userresponse(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class userlogin(BaseModel):
    email: EmailStr
    password: str

class adminlogin(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class token(BaseModel):
    access_token : str
    token_type: str

class token_data(BaseModel):
    id : Optional[str] = None

class inputschema(BaseModel):
    id: int
    name: str

class epic(BaseModel):
    name: str
    epic_no: str


class voter(BaseModel):
    epic_no: str 
    name : str
    age : int
    father_name : str
    husband_name : str
    sex : str
    house_no : str
    poll_booth: int
    district : str
    state : str

class update_voter(BaseModel):
    epic_no: str
    updated_epic_no: str 
    name : str
    age : int
    father_name : str
    husband_name : str
    sex : str
    house_no : str
    poll_booth: int
    district : str
    state : str