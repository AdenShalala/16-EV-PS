from typing import Annotated
from fastapi import FastAPI, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher
import session
import database
import schema


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Hello bob"}

@app.get("/clinician")
async def get_clinician(token: Annotated[schema.PublicClinican, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    sess = session.validate_session(token=token)

    if not sess:
        raise credentials_exception
    
    clinician = database.get_clinician(sess.clinician_id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    return schema.PublicClinican(clinician.clinician_id, clinician.first_name, clinician.last_name, clinician.email, clinician.created_at)
    

@app.get("/patients")
async def get_patients(token: Annotated[list[schema.Patient], Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    sess = session.validate_session(token=token)

    if not sess:
        raise credentials_exception
    
    if sess.account_type != "Clinician":
        raise credentials_exception

    clinician = database.get_clinician(sess.clinician_id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    patients = database.get_patients_from_clinician(clinician)
    
    return patients

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    clinician = database.get_clinician_from_email(form_data.username)

    print(clinician)

    if not clinician:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    ph = PasswordHasher()
    if not ph.verify(clinician.password, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    _, token = session.create_session(clinician.clinician_id, "clinician")
    return {"access_token": token, "token_type": "bearer"}