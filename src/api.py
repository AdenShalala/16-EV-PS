from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from argon2 import PasswordHasher
from nicegui import app as app, ui
import sessions
import database
from schema import *

# OAuth2 password-bearer scheme. Clients will first POST to /token to get a bearer token,
# then send it as "Authorization: Bearer <token>" on every request.
# tokenUrl="token" means our token endpoint is /api/token. Keep this in sync with the route below.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# exceptions
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    headers={"WWW-Authenticate": "Bearer"},
)
server_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal Server Error",
)

login_exception = HTTPException(status_code=400, detail="Incorrect username or password")




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
/patient/activity -> Creates an activity and returns it
/sensor -> Creates a sensor and returns it
/activityreading -> Creates an activity reading and returns it


GET
/me -> Returns the user information
/clinicians/{clinician_id} -> Returns a clinician (ADMIN ONLY)
/clinicians -> Returns all clinicians (ADMIN ONLY)

/patients/{patient_id} -> Returns a patient
/patients -> Returns all patients

/patients/{patient_id}/activities/{activity_id} -> Returns an activity
/patients/{patient_id}/activities -> Returns all activities

/patients/{patient_id}/sensors/{sensor_id} -> Returns a sensor
/patients/{patient_id}/sensors -> Returns all sensors

/patient/{patient_id}/activities/{activity_id}/readings/{reading_id} -> Returns an activity reading
/patient/{patient_id}/activities/{activity_id}/readings -> Returns all activity readings

/patient/{patient_id}/activities/{activity_id}/readings/{reading_id}/pressure/{pressure_reading_id} -> Returns a pressure reading
/patient/{patient_id}/activities/{activity_id}/readings/{reading_id}/pressure/ -> Returns all pressure readings

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

@app.post("/api/token")
def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
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

@app.post("/api/clinician")
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

@app.post("/api/patient")
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

###############
# GET METHODS #
###############
@app.get('/api/logout')
def logout(token: Annotated[Clinician | Admin, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    
    if not account:
        raise server_exception

    sessions.delete_session(session)
    return 200



@app.get('/api/me')
def get_me(token: Annotated[Clinician | Admin, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    
    if not account:
        raise server_exception

    return account

@app.get("/api/clinicians/{clinician_id}")
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

@app.get("/api/clinicians")
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
    
@app.get("/api/patients/{patient_id}")
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
        
@app.get("/api/patients")
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

@app.get("/api/patients/{patient_id}/activities")
def get_activities(patient_id: str, token: Annotated[Activity, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception
    
    try:
        return database.get_activities_from_patient_id(patient_id)
    except:
        raise server_exception

@app.get("/api/patients/{patient_id}/activities/{activity_id}")
def get_activity(patient_id: str, activity_id: str, token: Annotated[Activity, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception
    
    try:
        return database.get_activity(activity_id)
    except:
        raise server_exception


@app.get("/api/patients/{patient_id}/sensors/{sensor_id}")
def get_sensor(patient_id: str, sensor_id: str, token: Annotated[Activity, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception
    
    try:
        return database.get_sensor(sensor_id)
    except:
        raise server_exception

@app.get("/api/patients/{patient_id}/sensors")
def get_sensors(patient_id: str, sensor_id: str, token: Annotated[Activity, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception
    

    try:
        return database.get_sensors_from_patient_id(patient_id)
    except:
        raise server_exception


@app.get("/api/patients/{patient_id}/activities/{activity_id}/readings/")
def get_activity_readings(patient_id: str, activity_id: str, token: Annotated[list[ActivityReading], Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception

    try:
        return database.get_activity_readings_from_activity_id(activity_id)
    except:
        raise server_exception  
    

@app.get("/api/patients/{patient_id}/activities/{activity_id}/readings/{reading_id}/pressure")
def get_pressure_readings(patient_id: str, activity_id: str, reading_id: str, token: Annotated[list[ActivityReading], Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    if not account:
        raise server_exception

    if type(account) == Clinician:
        patients = get_patients(token=token)

        found = False
        
        for patient in patients:
            if patient.patient_id == patient_id:
                found = True
                break

        if not found:
            raise unauthorized_exception

    try:
        return database.get_pressure_readings_from_reading_series_id(reading_id)
    except:
        raise server_exception  