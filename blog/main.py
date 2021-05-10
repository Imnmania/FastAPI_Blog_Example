from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

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
@app.get('/blog', status_code=status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#======================== GET SINGLE BLOG USING ID ==================#
@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not available'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )
    return blog


#======================== DELETE SINGLE BLOG USING ID ==================#
@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with id {id} not available'
            )
    return {'detail': 'Delete Successful'}
