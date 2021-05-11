from pydantic import BaseModel

# @app.post('/blog')
# def create(title, body):
#     return {'title': title, 'body': body}

#========================== REQUEST BODY MODELS/ SCHEMAS ========================#
class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(Blog):
    class Config:
        orm_mode = True

