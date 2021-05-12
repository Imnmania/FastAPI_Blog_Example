from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi import APIRouter
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
### repository
from ..repository import blogRepo


router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)



#============================ GET ALL BLOGS =============================#
# @app.get('/blog', status_code=status.HTTP_200_OK)
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepo.get_all_blogs(db)



#============================ CREATE BLOG ==============================#
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepo.create_blog(db, request)



#======================== GET SINGLE BLOG USING ID ==================#
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepo.get_blog_by_id(id, db)



#======================== DELETE SINGLE BLOG USING ID ==================#
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepo.delete_blog(id, db)




#========================= UPDATE SINGLE BLOG USING ID ===================#
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogRepo.update_blog(id, request, db)
   