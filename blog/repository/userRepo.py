from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from .. import models
from ..hashing import Hash


#========================== CREATE USER ============================#
def create_user(db, request):
    # hashedPassword = pwd_ctx.hash(request.password)
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#=========================== GET ALL USERS ===========================#
def get_all_users(db):
    users = db.query(models.User).all()
    return users


#=========================== GET SINGLE USER WITH ID ===========================#
def get_single_user(id, db):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"USER ID:{id} DOES NOT EXIST")

    return user



#========================== DELETE USER ============================#
def delete_user(id, db):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,\
                detail= f'USER DOES NOT EXIST'
        )

    user.delete(synchronize_session = False)
    db.commit()
    
    return 'DELETE COMPLETE'


#============================= UPDATE USER ============================#
def update_user(id, request, db):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER DOES NOT EXIST")

    user.update(jsonable_encoder(request), synchronize_session = False)
    db.commit()

    return {'detail': 'Update Successful'}
