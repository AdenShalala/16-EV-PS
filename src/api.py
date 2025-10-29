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

'''
THIS IS NOT ACCURATE; THIS IS WHAT A PROPOSED REDESIGN IS
PLEASE VISIT /docs FOR THE REAL API
POST
/login -> Creates a Session and returns it
/logout -> Deletes current session
/clinician -> Creates a Clinician and returns it (Admin)
/patients -> Creates a Patient and returns it
/activities -> Creates an Activity and returns it
/sensors -> Creates a Sensor and returns it
/activity_readings -> Creates an ActivityReading and returns it
/pressure_readings -> Creates a PressureReading and returns it

GET
/me -> Returns the user information
/clinicians/{clinician_id} -> Returns a Clinician
/clinicians -> Returns all Clinicians (Admin)
/patients/{patient_id} -> Returns a Patient
/patients -> Returns all Patients
/activities/{activity_id} -> Returns an Activity
/activities -> Returns all Activities
/sensors/{sensor_id} -> Returns a Sensor
/sensors -> Returns all Sensors
/activity_readings/{reading_id} -> Returns an ActivityReading
/activity_readings -> Returns all ActivityReadings
/pressure_readings/{pressure_reading_id} -> Returns a PressureReading
/pressure_readings -> Returns all PressureReadings

/graph_data -> Special endpoint, returns filtered graph data

PUT
/me -> Updates user information
/clinicians/{id} -> Update a Clinician
/patients/{id} -> Update a Patient
/activities/{id} -> Update an Activity
/sensors/{id} -> Update a Sensor
/activity_readings/{id} -> Update an ActivityReading
/pressure_readings/{id} -> Update a Sensor

DELETE
/me -> Deletes current user
/clinicians/{id} -> Deletes a Clinician
/patients/{id} -> Deletes a Patient
/activities/{id} -> Deletes an Activity
/sensors/{id} -> Deletes a Sensor
/activity_readings/{id} -> Deletes an ActivityReading
/pressure_readings/{id} -> Deletes a Sensor
'''

# OAuth2 password-bearer scheme. Clients will first POST to /token to get a bearer token,
# then send it as "Authorization: Bearer <token>" on every request.
# tokenUrl="token" means our token endpoint is /api/token. Keep this in sync with the route below.

api_version = "/api/v1/"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=api_version + "token")

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

def verify_email(email: str):
    result = database.get_clinician_from_email(email)

    if result:
        return False
    else:
        return True
    
def verify_patient_email(email: str):
    result = database.get_patient_from_email(email)

    if result:
        return False
    else:
        return True    

def verify_admin_email(email: str):
    result = database.get_admin_from_email(email)

    if result:
        return False
    else:
        return True



################
# POST METHODS #
################
@app.post("/api/token")
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

@app.post('/api/logout')
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    
    if not account:
        raise server_exception

    sessions.delete_session(session)
    return 200

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
def post_patient(patient: Patient, token: Annotated[str, Depends(oauth2_scheme)]):
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
@app.get('/api/me')
def get_me(token: Annotated[str, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)
    
    if not account:
        raise server_exception

    return account

@app.get("/api/clinicians/{clinician_id}")
def get_clinician(clinician_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_clinicians(token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_patient(patient_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_patients(token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_activities(patient_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_activity(patient_id: str, activity_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_sensor(patient_id: str, sensor_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_sensors(patient_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_activity_readings(patient_id: str, activity_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
def get_pressure_readings(patient_id: str, activity_id: str, reading_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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

@app.get("/api/graph_data")
def get_graph_data(activity_id: str, patient_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
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
        return database.get_pressure_readings_for_activities(activity_id, patient_id)
    except:
        raise server_exception     

@app.put("/api/me")
def put_me(updated_account: Clinician | Admin, token: Annotated[str, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)   

    if not account:
        raise server_exception

    if type(account) == Clinician:
        try:
            database.update_clinician(updated_account)
        except: 
            raise server_exception
    else:
        try:
            database.update_admin(updated_account)
        except: 
            raise server_exception
        
@app.put("/api/patient/{patient_id}")
def put_patient(patient_id: str, updated_patient: Patient, token: Annotated[str, Depends(oauth2_scheme)]):
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
        database.update_patient(updated_patient)
    except: 
        raise server_exception
    
@app.put("/api/patient/{patient_id}")
def put_clinician(clinician_id: str, updated_clinician: Clinician, token: Annotated[str, Depends(oauth2_scheme)]):
    session = sessions.validate_session(token=token)

    if not session:
        raise credentials_exception
    
    account = get_account(session.id)   

    if not account:
        raise server_exception
    
    if type(account) != Admin:
        raise unauthorized_exception    

    try:
        database.update_clinician(updated_clinician)
    except: 
        raise server_exception