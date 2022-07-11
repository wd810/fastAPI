'''
User sections
'''
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # hash password- user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    exist_email = db.query(models.User).filter(models.User.email == new_user.email).first()
    if exist_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email {new_user.email} has been registered already")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users/{id}', response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user id {id} does not found')

    return user