from pydantic import BaseModel, validator
from typing import Optional
#for future  use ............
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

    @validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError('Invalid email address')
        return v

    class Config:
        anystr_strip_whitespace = True
