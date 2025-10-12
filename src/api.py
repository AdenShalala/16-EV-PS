from typing import Annotated
from fastapi import FastAPI, Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from argon2 import PasswordHasher
from nicegui import app as app, ui
import sessions
import database
from schema import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

server_exception = HTTPException(
            status_code=500,
            detail="Internal Server Error"
)

login_exception = HTTPException(status_code=400, detail="Incorrect username or password")

unauthorized_exception = HTTPException(status_code=401, detail="Unauthorized")


# yes i know these two functions are ugly 6️⃣7️⃣
def get_account(id: str) -> Clinician | Admin:
    clinician = database.get_clinician(id)
    admin = database.get_admin(id)

    if not clinician and not admin:
        return None
    if not clinician and admin:
        return admin
    if not admin and clinician:
        return clinician
    else:
        # ????
        return clinician, admin

def get_account_by_email(email: str) -> Clinician | Admin:
    clinician = database.get_clinician_from_email(email=email)
    admin = database.get_admin_from_email(email=email)

    if not clinician and not admin:
        return None
    if not clinician and admin:
        return admin
    if not admin and clinician:
        return clinician
    else:
        # ????
        return clinician, admin

'''
POST
/login -> Creates a session and returns it
/clinician -> Creates a clinican and returns it (ADMIN ONLY)
/patient -> Creates a patient and returns it
/activity -> Creates an activity and returns it
/sensor -> Creates a sensor and returns it
/sensorreading -> Creates a sensor reading and returns it
/activityreading -> Creates an activity reading and returns it


GET
/me -> Returns the user information
/clinician/{id} -> Returns a clinician (ADMIN ONLY)
/clinicians -> Returns all clinicians (ADMIN ONLY)

/patient/{id} -> Returns a patient
/patients -> Returns all patients

/activity/{id} -> Returns an activity
/activities -> Returns all activities

/sensor/{id} -> Returns a sensor
/sensors -> Returns all sensors

/sensorreading/{id} -> Returns a sensor reading
/sensorreadings -> Returns all sensor readings

PUT
/me -> Updates user information
/clinician/{id} -> Update a clinician (ADMIN ONLY)
/patient/{id} -> Update a patient
/activity/{id} -> Update an activity
/sensor/{id} -> Update a sensor

DELETE: Err see if i need this.

'''

################
# POST METHODS #
################

@app.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    account = get_account_by_email(email=form_data.username)
    
    ph = PasswordHasher()

    try:
        ph.verify(account.password, form_data.password)
    except:
        raise login_exception
    
    id: str
    account_type = type(account).__name__

    if type(account) is Clinician:
        id = account.clinician_id
    else:
        id = account.admin_id
    
    try:
        _, token = sessions.create_session(id, account_type)

        return {"access_token": token, "token_type": "bearer", "type": account_type}    
    except:
        raise server_exception

@app.post("/clinician")
def post_clinician(clinician: Clinician, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    # Admin only
    if session.account_type != "Admin":
        raise credentials_exception
    
    admin = database.get_admin(session.id)
    if not admin:
        raise server_exception

    try:
        database.write_clinician(clinician=clinician)
    except:
        raise server_exception

@app.post("/patient")
def post_patient(patient: Patient, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    # Make sure if its a clinician posting, that they can only add patients to themselves
    if type(account) == Clinician:
        if patient.clinician_id != account.clinician_id:
            raise unauthorized_exception

    try: 
        database.write_patient(patient)    
    except:
        raise server_exception
    
    return patient

@app.post("/activity")
def post_activity(activity: Activity, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        # Check patients from clinician then check if activity.patient_id is in that list
        patients = get_patients(token=token)

        found = False

        for patient in patients:
            if activity.patient_id == patient.patient_id:
                found = True
                print(patient)
                break
        if not found:
            raise unauthorized_exception

    try: 
        database.write_activity(activity)
    except:
        raise server_exception    
    
    return activity

# @app.post("/sensor")
# def post_sensor(sensor: Sensor, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
#     if not account:
#         raise server_exception

#     if type(account) == Clinician:
#         if patient.clinician_id != account.clinician_id:
#             raise unauthorized_exception

#     try: 
#         database.write_patient(patient)
#         patient = database.get_patient(patient.patient_id)
#         return patient
#     except:
#         raise server_exception

# @app.post("/pressurereading")
# def post_pressure_reading(pressure_reading: PressureReading, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
#     if not account:
#         raise server_exception

#     if type(account) == Clinician:
#         if patient.clinician_id != account.clinician_id:
#             raise unauthorized_exception

#     try: 
#         database.write_patient(patient)
#         patient = database.get_patient(patient.patient_id)
#         return patient
#     except:
#         raise server_exception

# @app.post("/activityreading")
# def post_activity_reading(activity_reading: ActivityReading, token: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
#     if not account:
#         raise server_exception

#     if type(account) == Clinician:
#         if patient.clinician_id != account.clinician_id:
#             raise unauthorized_exception

#     try: 
#         database.write_patient(patient)
#         patient = database.get_patient(patient.patient_id)
#         return patient
#     except:
#         raise server_exception


###############
# GET METHODS #
###############

@app.get('/me')
def get_me(token: Annotated[Clinician | Admin, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    
    if not account:
        raise server_exception

    return account

@app.get("/clinicians/{clinician_id}")
def get_clinician(clinician_id: str, token: Annotated[Clinician, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    if not session.account_type == "Admin":
        raise credentials_exception
    
    admin = database.get_admin(session.id)
    
    if not admin:
        raise server_exception
    
    try:
        clinician = database.get_clinician(clinician_id)

        if not clinician:
            raise HTTPException(
                status_code=404,
                detail="Could not find clinician"   
            )
    
        return clinician
    except:
        raise server_exception

@app.get("/clinicians")
def get_clinicians(token: Annotated[Clinician, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    if not session.account_type == "Admin":
        raise credentials_exception
    
    admin = database.get_admin(session.id)
    
    if not admin:
        raise server_exception
    
    try:
        clinicians = database.get_clinicians()
        return clinicians
    except:
        raise server_exception
    
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str, token: Annotated[Patient, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception
    
    patient_not_found = HTTPException(
        status_code=404,
        detail="Could not find patient"   
    )

    if type(account) == Clinician:
        try:
            patient = database.get_patient_from_clinician(patient_id, account)

            if not patient:
                raise patient_not_found
        
            return patient
        except:
            raise server_exception        
    elif type(account) == Admin:
        try:
            patient = database.get_patient(patient_id)

            if not patient:
                raise patient_not_found
        
            return patient
        except:
            raise server_exception
        
@app.get("/patients")
def get_patients(token: Annotated[list[Patient], Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        try:
            return database.get_patients_from_clinician(account)
        except:
            raise server_exception        
    elif type(account) == Admin:
        try:
            return database.get_patients()
        except:
            raise server_exception
        

###############
# PUT METHODS #
###############
# @app.put('/me')
# def put_me(token: Annotated[Clinician | Admin, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
    
#     if not account:
#         raise server_exception

#     return account

# @app.put('/clinician/{clinician_id}')
# def put_clinician(clinician_id: str, token: Annotated[Clinician, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
    
#     if not account:
#         raise server_exception

#     return account

# @app.put('/patient/{patient_id}')
# def put_patient(patient_id: str, patient: Patient token: Annotated[Patient, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
    
#     if not account:
#         raise server_exception

#     return account

# @app.put('/activity/{activity_id}')
# def put_activity(activity_id: str, activity: Activity, token: Annotated[Patient, Depends(oauth2_scheme)]):
#     session = sessions.validate_session(token=token)

#     if not session:
#         raise credentials_exception
    
#     account = get_account(session.id)
    
#     if not account:
#         raise server_exception

#     return account