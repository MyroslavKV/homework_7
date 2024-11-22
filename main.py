from fastapi import FastAPI, Query, status
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
import re

app = FastAPI()

class User(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)
    phone_number: str

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str, field_name: str):
        if not value.isalpha():
            raise ValueError(f"The field must contain only letters.")
        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value=str):
        if not re.search(r"[A-Z]", value):
            raise ValueError("The password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("The password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("The password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("The password must contain at least one special character.")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        if not (10 <= len(value) <= 15):
            raise ValueError("The length of the phone number must be between 10 and 15 characters.")
        
        if not value.startswith('+') and not value.isdigit():
            raise ValueError("The phone number must consist of only digits or start with '+'.")
        
        if value.startswith('+') and not value[1:].isdigit():
            raise ValueError("The phone number after '+' must contain only numbers.")
        return value
    



@app.get("/")
async def root():
    return RedirectResponse("/docs")

@app.post("/register/")
async def register_user(user: User):
    response = {
        "message": "User registred",
        "user_data": user.model_dump(),
    }
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)