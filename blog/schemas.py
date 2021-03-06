from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import List

from sqlalchemy.sql.sqltypes import Integer

# @app.post('/blog')
# def create(title, body):
#     return {'title': title, 'body': body}

#========================== REQUEST BODY MODELS/ SCHEMAS ========================#



#========================== BLOG BASE MODEL =========================#
class Blog(BaseModel):
    title: str
    body: str


#========================== USER BASE MODEL =========================#
class User(BaseModel):
    username: str
    email: str
    password: str


#========================== BLOG FOR USER RESPONSE ====================#
class BlogForUser(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True

#========================== USER FOR BLOG RESPONSE ====================#
class UserForBlog(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True






# CREATING CUSTOM RESPONSE MODELS

#=========================== USER RESPONSE MODEL ========================#
class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[BlogForUser] = []

    class Config:
        orm_mode = True


#=========================== BLOG RESPONSE MODEL ========================#
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserForBlog

    class Config:
        orm_mode = True
