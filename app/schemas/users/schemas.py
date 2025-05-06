from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    username:str
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
