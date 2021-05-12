from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import List

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
    title: str
    body: str

    class Config:
        orm_mode = True

#========================== USER FOR BLOG RESPONSE ====================#
class UserForBlog(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True






# CREATING CUSTOM RESPONSE MODELS
class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[BlogForUser] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserForBlog

    class Config:
        orm_mode = True
