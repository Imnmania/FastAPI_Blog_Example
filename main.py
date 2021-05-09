from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f'{limit} published blog from db'}
    else:
        return {"data": f'{limit} blogs from db'}
    

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished work'}

@app.get('/blog/{id}')
def show(id: int):
    """fetch blog with id = id"""
    return {"data": id}

@app.get('/blog/{id}/comments')
def comments(id: int, limit: Optional[int] = 0):
    # fetch comments with blog id = id
    # return {'data': {'1', '2'}}
    # return limit
    return {'data': {'id': id, 'numList': {'1', '2'}}}



