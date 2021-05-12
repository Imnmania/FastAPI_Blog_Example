from sqlalchemy.orm.session import Session
from .. import schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter(
    tags = ['Authentication'],
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='INVALID USERNAME')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='INVALID PASSWORD')

    # generate jwt token

    return user