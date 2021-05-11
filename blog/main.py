from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from .hashing import Hash
# from passlib.context import CryptContext

#========================= Initialize fastapi ==========================#
app = FastAPI()


#===================== CHECK EXISTING/ CREATE TABLES ===================#
models.Base.metadata.create_all(engine)


#========================= GET DB FOR SESSION ==========================#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#============================ CREATE BLOG ==============================#
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    # return request
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#============================ GET ALL BLOGS =============================#
# @app.get('/blog', status_code=status.HTTP_200_OK)
@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#======================== GET SINGLE BLOG USING ID ==================#
@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not available'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )
    return blog.first()


#======================== DELETE SINGLE BLOG USING ID ==================#
@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )

    blog.delete(synchronize_session = False)
    db.commit()

    return {'detail': 'Delete Successful'}



#========================= UPDATE SINGLE BLOG USING ID ===================#
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)\

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )
    
    blog.update(jsonable_encoder(request), synchronize_session = False)
    db.commit()
    
    return {'detail': 'Update Successful'}




# #========================= HASHING PASSWORD ========================#
# pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')



#========================== CREATE USER ============================#
@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    # hashedPassword = pwd_ctx.hash(request.password)

    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user