import database
import secrets
import hashlib
import hmac
from schema import *
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token():
    return secrets.token_urlsafe(24)

def hash_secret(secret: str):
    hash_object = hashlib.sha256()
    #print(hash_object)
    hash_object.update(secret.encode('utf-8'))
    return hash_object.digest()

def create_session():
    time = datetime.now()
    id = generate_token()
    secret = generate_token()
    hashed_secret = hash_secret(secret)
    token = id + "." + secret

    session = Session(id, hashed_secret, time)

    database.write_session(session)

    #print(session)
    return session, token

def validate_token(token: str):
    #print(token)
    split = token.split('.');

    if (len(split) != 2):
        return None
    
    session = database.get_session(split[0])
    if session == None:
        return None
    
    # timeout = 1 week (can adjust)
    print((datetime.now() - session.created_at).days)
    if (datetime.now() - session.created_at).days > 7:
        # delete
        database.delete_session(session.session_id)
        return None
    
    hashed_secret = hash_secret(split[1])

    valid = hmac.compare_digest(session.secret_hash, hashed_secret)
    if not valid:
        return None
    
    return session

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_clinician(email: str, password: str):
    clinician = database.get_clinician_from_email(email)
    if not clinician:
        return False
    if not verify_password(password, clinician.password):
        return False
    return clinician

    
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.email}, expires_delta=access_token_expires
    # )
    #return Token(access_token=access_token, token_type="bearer")

def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> str:
    user = authenticate_clinician(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    session, token = create_session()
    return token