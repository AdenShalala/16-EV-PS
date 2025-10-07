from typing import Annotated
from fastapi import FastAPI, Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from argon2 import PasswordHasher
from nicegui import app as app, ui
import session
import database
from schema import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def middleware(token: str): 
    sess = session.validate_session(token=token)

    if not sess:
        raise credentials_exception
    
    return sess


@app.get("/clinician")
def get_clinician(token: Annotated[PublicClinican, Depends(oauth2_scheme)]):
    sess = middleware(token)

    if sess.account_type != "Clinician":
        raise credentials_exception
    
    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    return PublicClinican(clinician.clinician_id, clinician.first_name, clinician.last_name, clinician.email, clinician.created_at)
    

@app.get("/patients")
def get_patients(token: Annotated[list[Patient], Depends(oauth2_scheme)]):
    sess = middleware(token)
    
    if sess.account_type != "Clinician":
        raise credentials_exception

    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    patients = database.get_patients_from_clinician(clinician)
    
    return patients

@app.get("/patient")
def get_patient(patient_id, token: Annotated[Patient, Depends(oauth2_scheme)]):
    sess = middleware(token)
    
    if sess.account_type != "Clinician":
        raise credentials_exception

    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    patient = database.get_patient_from_clinician(patient_id, clinician)
    
    return patient    

@app.get("/activities")
def get_activities(token: Annotated[list[Activity], Depends(oauth2_scheme)]):
    sess = middleware(token)
    
    if sess.account_type != "Clinician":
        raise credentials_exception

    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    activities = database.get_activities_from_clinician(clinician)
    
    return activities

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    clinician = database.get_clinician_from_email(form_data.username)

    if not clinician:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    ph = PasswordHasher()

    if not ph.verify(clinician.password, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    _, token = session.create_session(clinician.clinician_id, "Clinician")
    return {"access_token": token, "token_type": "bearer"}
