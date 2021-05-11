from fastapi.param_functions import Body
from pydantic import BaseModel

# @app.post('/blog')
# def create(title, body):
#     return {'title': title, 'body': body}

#========================== REQUEST BODY MODELS/ SCHEMAS ========================#
class Blog(BaseModel):
    title: str
    body: str

# # EXTENDING PREVIOUS MODELS
# class ShowBlog(Blog):
#     class Config:
#         orm_mode = True

# CREATING CUSTOM RESPONSE MODELS
class ShowBlog(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True



#========================== USER =========================#
class User(BaseModel):
    username: str
    email: str
    password: str


class ShowUser(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True