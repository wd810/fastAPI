from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credential: schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials.")

    # verify password with hash function
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials.")

    # create a token: put 'user_id' to payload
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    # return the token
    return {"token": access_token, "token_type": "bearer"}