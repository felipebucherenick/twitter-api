# Python
from datetime import date, datetime
from uuid import UUID
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI

app = FastAPI()

# User Models --------------------------------------


class UserBase(BaseModel):
    user_id: UUID = Field(...),
    email: EmailStr = Field(...),


class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    ),


class User(UserBase):
    first_name: str = Field(
        ...,
        min_items=1,
        max_length=50
    ),
    last_name: str = Field(
        ...,
        min_items=1,
        max_length=50
    ),
    birth_date: Optional[date] = Field(default=None)

# Tweet Model --------------------------------------------


class Tweet(BaseModel):
    tweet_id: UUID = Field(...),
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    ),
    created_at: datetime = Field(default=datetime.now()),
    updated_at: Optional[datetime] = Field(default=None),
    by: User = Field(...)


@app.get(path='/')
def home():
    return {'Twitter API': 'Working'}
