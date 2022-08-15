from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, auth2


router = APIRouter(tags=['Authentication'])


@router.post('/api/login', response_model=schemas.Token)
# MUST TO PUT DATA INTO BODY -> FORM
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm has fields username(instead email) and password
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    # verify automaticlly hashing user_credentials.password and verify with hashed user.password in db
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    # CREATE A TOKEN AND RETURN            WE CAN PUT DATA WHICH WE WANT
    access_token = auth2.create_access_token(data={"user_id": user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
