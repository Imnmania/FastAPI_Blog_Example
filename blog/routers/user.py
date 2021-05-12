from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi import APIRouter
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..hashing import Hash

### Repository Import
from ..repository import userRepo




router = APIRouter(
    tags=['Users'],
    prefix='/user'
)



#========================== CREATE USER ============================#
@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return userRepo.create_user(db, request)


#=========================== GET ALL USERS ===========================#
@router.get('/', status_code=status.HTTP_200_OK, response_model = List[schemas.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    return userRepo.get_all_users(db)



#=========================== GET SINGLE USER WITH ID ===========================#
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model = schemas.ShowUser)
def get_single_user(id, db: Session = Depends(get_db)):
    return userRepo.get_single_user(id, db)


#========================== DELETE USER ============================#
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id, db: Session = Depends(get_db)):
    return userRepo.delete_user(id, db)


#========================== UPDATE USER ============================#
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id, request: schemas.User, db: Session = Depends(get_db)):
    return userRepo.update_user(id, request, db)
