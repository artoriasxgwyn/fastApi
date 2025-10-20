from pydantic import BaseModel, EmailStr#toca descargarlo con pip install email-validator y es para validar emails
from typing import Optional

class User(BaseModel):
    id: Optional[str]=None
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    name: str
    password: str
