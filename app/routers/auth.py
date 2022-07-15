from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schema, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schema.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm contains: username and password ...
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")

    # verify password with hash function
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials.")

    # create a token: 'user_id' => to payload
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    # return the token
    return {"access_token": access_token, "token_type": "bearer"}