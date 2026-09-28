from pydantic import BaseModel as pydantic_model, EmailStr
from typing import Optional


class LoginUser(pydantic_model):
    username : str
    password : str

class LoginAdmin(pydantic_model):
    adminname: str
    password : str

class User_data(pydantic_model):
    username: Optional[str] = None
    email: Optional[str] = None

class Bio_content(pydantic_model):
    content:Optional[str] = None
class User_name(pydantic_model):
    username:str

class Id(pydantic_model):
    id:str

class Message(pydantic_model):
    message:str
