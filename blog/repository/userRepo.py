from fastapi import status, HTTPException
from .. import models
from ..hashing import Hash


def create_user(db, request):
    # hashedPassword = pwd_ctx.hash(request.password)
    new_user = models.User(username = request.username, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_users(db):
    users = db.query(models.User).all()
    return users

def get_single_user(id, db):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"USER ID:{id} DOES NOT EXIST")

    return user