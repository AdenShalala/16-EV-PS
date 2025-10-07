from typing import Annotated
from fastapi import FastAPI, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from nicegui import app as app, ui
from argon2 import PasswordHasher
import session
import asyncio
import database
import schema
import pages.login
import requests
from pages.header import header

#app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/clinician")
def get_clinician(token: Annotated[schema.PublicClinican, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    sess = session.validate_session(token=token)

    if not sess:
        raise credentials_exception
    
    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    return schema.PublicClinican(clinician.clinician_id, clinician.first_name, clinician.last_name, clinician.email, clinician.created_at)
    

@app.get("/patients")
def get_patients(token: Annotated[list[schema.Patient], Depends(oauth2_scheme)]):
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

    clinician = database.get_clinician(sess.id)
    if not clinician:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
    patients = database.get_patients_from_clinician(clinician)
    
    return patients

@app.get("/activities")
def get_activities(token: Annotated[list[schema.Activity], Depends(oauth2_scheme)]):
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

#@app.post("/admin")


@ui.page('/test')
def test():
    # comparing entered value
    def checkLogin():
        x = login(OAuth2PasswordRequestForm(password=password.value, username=email.value))

        print(x)
        app.storage.user['token'] = x['access_token']
        
        print(get_patients(token=app.storage.user['token']))

        


    def awesome():
        print(app.storage.user["token"])

        #Homepage.mainNavigate()
    ui.page_title("SocketFit Dashboard")
    header()
    
    with ui.row().classes('w-full h-full justify-center items-center'):
        # login box
        with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
            email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] left-2')
            password = ui.input(placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
            ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')
            ui.button("TEST", on_click=awesome, color='#FFB030').classes('w-full text-white')
            #ui.button('Login as IT Admin', color='#3545FF', on_click=DatabaseConfig.navigateConfig).classes('w-full text-white')

ui.run(fastapi_docs=True, storage_secret="HELPPP")