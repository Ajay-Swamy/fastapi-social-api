from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional,Annotated

#--------------------------Posts-------------------------------
class PostBase(BaseModel):
    title:str
    content:str
    published:bool =True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime


class Post(PostBase):
    id: int
    created_at:datetime
    owner_id:int
    owner:UserOut

    class Config:
        orm_mode=True

class PostOut(BaseModel):
     Post:Post
     votes:int
     class Config:
        from_attributes = True

#------------------------Users-----------------------------------

class UserCreate(BaseModel):
    email:EmailStr
    password:str



    class Config:
            orm_mode=True


#--------------------------User Login-----------------------------

class UserLogin(BaseModel):
     email:EmailStr
     password: str


class Token(BaseModel):
     access_token:str
     token_type:str


class TokenData(BaseModel):
     id:Optional[int]=None

class Vote(BaseModel):
     post_id:int
     dir: Annotated[int,Field(le=1)]
     