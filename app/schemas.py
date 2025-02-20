import re
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class UserBase(BaseModel):
    username: str

# class UserCreate(UserBase):
#     password: str

class UserCreate(UserBase):
    password: str

    @validator("username")
    def validate_username(cls, value):
        if not re.fullmatch(r"^[A-Za-z]{3,}$", value):
            raise ValueError("Username must contain at least 3 characters, only alphabets, and no spaces or special characters.")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character.")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value

class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, error_messages={"required": "Username is required"})
    password: str = Field(..., min_length=1, error_messages={"required": "Password is required"})

