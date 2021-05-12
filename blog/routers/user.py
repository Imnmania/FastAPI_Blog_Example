from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi import APIRouter
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..hashing import Hash




router = APIRouter()



#========================== CREATE USER ============================#
@router.post('/user', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    # hashedPassword = pwd_ctx.hash(request.password)

    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#=========================== GET ALL USERS ===========================#
@router.get('/user', status_code=status.HTTP_200_OK, response_model = List[schemas.ShowUser], tags=['Users'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users



#=========================== GET SINGLE USER WITH ID ===========================#
@router.get('/user/{id}', status_code=status.HTTP_200_OK, response_model = schemas.ShowUser, tags=['Users'])
def get_single_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"USER ID:{id} DOES NOT EXIST")

    return user