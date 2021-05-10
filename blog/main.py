from fastapi import FastAPI, Depends
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
@app.post('/blog')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    # return request
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


#============================ GET ALL BLOGS =============================#
@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


#======================== GET SINGLE BLOG USING ID ==================#
@app.get('/blog/{id}')
def get_blog_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
