from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi import APIRouter
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder



router = APIRouter()



#============================ GET ALL BLOGS =============================#
# @app.get('/blog', status_code=status.HTTP_200_OK)
@router.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['Blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



#============================ CREATE BLOG ==============================#
@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    # return request
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



#======================== GET SINGLE BLOG USING ID ==================#
@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blogs'])
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
@router.delete('/blog/{id}', status_code=status.HTTP_200_OK, tags=['Blogs'])
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
@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
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