import datetime
import re
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime 

class UserBase(BaseModel):
    name:str
    email: str
    username: str
    @field_validator("email")
    def check_email(cls, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value
    
    
    @field_validator("username")
    def check_username(cls,value):
        if len(value) < 5:
            raise ValueError("Username must be at least 5 characters long")
        if not any(char.isalpha() for char in value):
            raise ValueError("Username must contain at least one letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Username must contain at least one digit")
        return value
    
class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True
        arbitrary_types_allowed = True




class UserInDB(UserInDBBase):
    hashed_password: str


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] =None
    completed: bool = False
    due_date: Optional[datetime] = None
    

class Todo(TodoCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    



    class ConfigDict:
        from_attributes = True
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str