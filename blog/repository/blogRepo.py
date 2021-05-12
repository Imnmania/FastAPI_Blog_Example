from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from .. import models
from fastapi.encoders import jsonable_encoder


#============================ GET ALL BLOGS =============================#
def get_all_blogs(db):
    blogs = db.query(models.Blog).all()
    return blogs

#============================ CREATE BLOG ==============================#
def create_blog(db, request):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#======================== GET SINGLE BLOG USING ID ==================#
def get_blog_by_id(id, db):
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
def delete_blog(id, db):
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
def update_blog(id, request, db):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )
    
    blog.update(jsonable_encoder(request), synchronize_session = False)
    db.commit()
    
    return {'detail': 'Update Successful'}