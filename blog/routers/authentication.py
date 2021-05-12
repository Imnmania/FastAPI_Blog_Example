from sqlalchemy.orm.session import Session
from .. import schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..token import create_access_token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ['Authentication'],
)

@router.post('/login')
# def login(request: schemas.Login, db: Session = Depends(get_db)):
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='INVALID USERNAME')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='INVALID PASSWORD')

    # generate jwt token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

    return user