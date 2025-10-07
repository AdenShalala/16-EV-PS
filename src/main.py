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
import pages.utilities as utilities

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

@app.get("/patient")
def get_patient(patient_id, token: Annotated[schema.Patient, Depends(oauth2_scheme)]):
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
    
    patient = database.get_patient_from_clinician(patient_id, clinician)
    
    return patient    

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
        
        #print(get_patients(token=app.storage.user['token']))

        


    def awesome():
        print(app.storage.user["token"])

        #Homepage.mainNavigate()
    ui.page_title("SocketFit Dashboard")
    utilities.header()
    
    with ui.row().classes('w-full h-full justify-center items-center'):
        # login box
        with ui.card().classes('w-[300px] border rounded-md border-[#2C25B2]'):
            email = ui.input(placeholder='Email').classes('w-full border rounded-md border-[#3545FF] left-2')
            password = ui.input(placeholder='Password').classes('w-full border rounded-md border-[#3545FF]')
            ui.button('Login', on_click=checkLogin, color='#FFB030').classes('w-full text-white')
            ui.button("TEST", on_click=awesome, color='#FFB030').classes('w-full text-white')
            #ui.button('Login as IT Admin', color='#3545FF', on_click=DatabaseConfig.navigateConfig).classes('w-full text-white')




# creating new page
@ui.page('/main')
def main():
    def select(e):
        selected = e.value
        print(selected)

        if isinstance(selected, str) and selected.startswith('patient:'):
            id = selected.split(':')[1]
            app.storage.user["selected_patient"] = id
            return

    app.storage.user['current_page'] = '/main'

    patients = get_patients(token=app.storage.user["token"])

    ui.page_title("SocketFit Dashboard")
    genderList = ['All', 'Male', 'Female', 'Prefer not to say']
    amputationTypeList = ['All', 'Above Knee', 'Below Knee', 'Above Elbow', 'Below Elbow']
    

    utilities.header()
    with ui.row().classes('w-full'):
        ui.label("Welcome").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-full'):
        # side tree section
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
            current_page = app.storage.user.get('current_page', '')
            patient_nodes = []
            for patient in patients:
                full_name = f"{patient.first_name} {patient.last_name}"
                patient_nodes.append({
                    'id': f'patient:{patient.patient_id}',
                    'label': full_name
                })

            tree_data = [{
                'id': 'Patient Records',
                'label': utilities.bold('Patient Records') if current_page == '/main' else 'Patient Records',
                'children': patient_nodes,
            }]

            ui.tree(tree_data, label_key='label', on_select=select).expand(['Patient Records'])


        # main section
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            with ui.row().classes('w-full'):
                ui.label("Select User to View Users Information").classes('text-lg font-bold')
                ui.space()
                # box to search users
                search = ui.input(label="Search Name", placeholder='Name', on_change= lambda e: _on_search(e)).classes('border rounded-md border-[#FFB030]')
            ui.label("Filters").classes('text-md font-semibold')

            # filter titles
            with ui.grid(columns=10).classes('w-full gap-4'):
                ui.label("Height (cm):").classes('col-span-2')
                ui.label("Weight (kg):").classes('col-span-2')
                ui.label("Amputation Type:").classes('col-span-2')

            # filter boxes
            with ui.grid(columns=10).classes('w-full gap-4'):

                with ui.row().classes('col-span-2 gap-1'):

                    ui.add_head_html('''
                    <style>
                    input::placeholder {
                        text-align: center;
                    }
                    .q-field__label {
                        text-align: center !important;
                        width: 100% !important;
                    }
                    .q-select .q-field__input {
                        text-align: center !important;
                    }
                    </style>
                    ''')

                    # Height filters with on_change handlers
                    height_min = ui.number(label="Min", placeholder="Min", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')
                    height_max = ui.number(label="Max", placeholder="Max", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')

                with ui.row().classes('col-span-2 gap-1'):
                    # Weight filters with on_change handlers
                    weight_min = ui.number(label="Min", placeholder="Min", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')
                    weight_max = ui.number(label="Max", placeholder="Max", on_change=lambda e: _on_search(e)).classes('w-2/5 border rounded-md border-[#FFB030]').props('input-style="text-align: center"')

                amp_select = ui.select(value=amputationTypeList[0], options=amputationTypeList, on_change= lambda e: _on_search(e)).classes('col-span-2 border rounded-md border-[#FFB030]')

            cards_container = ui.column().classes('w-full')

            def _render_cards(p_list):
                cards_container.clear()
                with cards_container:
                    with ui.grid(columns=4).classes('w-full gap-6'):
                        for p in p_list:
                            full_name = f'{getattr(p, "first_name", "")} {getattr(p, "last_name", "")}'.strip()
                            with ui.card().classes('h-[150px] w-[160px] border border-[#2C25B2] cursor-pointer').on('click', lambda p=p: UserInformation.navigatePatient(p)):
                                ui.label(full_name or "Unnamed").classes('text-xl')
            
            def _filter_by_name(p_list, q):
                q = (q or '').strip().lower()
                if not q:
                    return p_list
                out = []
                for p in p_list:
                    fn = (getattr(p, 'first_name', '') or '').lower()
                    ln = (getattr(p, 'last_name', '') or '').lower()
                    full = f'{fn} {ln}'.strip()
                    if q in fn or q in ln or q in full:
                        out.append(p)
                return out
            
            def _filter_by_amputation(p_list, amp):
                amp = (amp or '').strip().lower()
                if not amp or amp == 'all':
                    return p_list
                out = []
                for p in p_list:
                    a = (getattr(p, 'amputation_type', '') or '').strip().lower()
                    if a == amp:
                        out.append(p)
                return out

            def _filter_by_height(p_list, min_height, max_height):
                out = []
                for p in p_list:
                    height = getattr(p, 'height', None)
                    if height is None:
                        continue
                    
                    # Convert height to number if it's a string
                    try:
                        height = float(height)
                    except (ValueError, TypeError):
                        continue
                    
                    # Check min height
                    if min_height is not None and height < min_height:
                        continue
                    
                    # Check max height
                    if max_height is not None and height > max_height:
                        continue
                    
                    out.append(p)
                return out

            def _filter_by_weight(p_list, min_weight, max_weight):
                out = []
                for p in p_list:
                    weight = getattr(p, 'weight', None)
                    if weight is None:
                        continue
                    
                    # Convert weight to number if it's a string
                    try:
                        weight = float(weight)
                    except (ValueError, TypeError):
                        continue
                    
                    # Check min weight
                    if min_weight is not None and weight < min_weight:
                        continue
                    
                    # Check max weight
                    if max_weight is not None and weight > max_weight:
                        continue
                    
                    out.append(p)
                return out
            
            def _apply_filters():
                base = app.storage.user.get('patients', [])
                
                # Apply name filter
                by_name = _filter_by_name(base, getattr(search, 'value', ''))
                
                # Apply amputation filter
                by_amp = _filter_by_amputation(by_name, getattr(amp_select, 'value', 'All'))
                
                # Apply height filter
                by_height = _filter_by_height(by_amp, getattr(height_min, 'value', None), getattr(height_max, 'value', None))
                
                # Apply weight filter
                by_weight = _filter_by_weight(by_height, getattr(weight_min, 'value', None), getattr(weight_max, 'value', None))
                
                _render_cards(by_weight)

            def _on_search(e):
                _apply_filters()

            _apply_filters()

def session_tree():
    current_page = app.storage.user.get('current_page', '')
    selected_patient_index = app.storage.user.get('selected_patient_index')

    seen_dates = OrderedDict()
    for activity in app.storage.user.get('activityList', []):
        start_raw = _get(activity, 'start_time')
        dt1 = _to_dt(start_raw)
        date_label = _date_label(dt1)
        
        # Use activity_id as the unique key (assuming it exists)
        activity_id = _get(activity, 'activity_id')  # or however you access the activity ID
        
        if activity_id not in seen_dates:
            # Combine date and activity type first, then apply bold to the whole thing
            full_label = date_label + " " + activity.type
            label = bold(full_label) if selected_session_date == activity_id else full_label
            seen_dates[activity_id] = {'id': activity_id, 'label': label}

    session_date_nodes = list(seen_dates.values())

    patient_nodes = []
    for i, patient in enumerate(app.storage.user.get('patients', [])):
        full_name = f"{patient.first_name} {patient.last_name}"
        patient_nodes.append({
            'id': f'patient-{i}',
            'label': full_name
        })

    expand_nodes = ['Patient Records']
    if current_page == '/sessionHistory' or current_page == '/activity':
        expand_nodes.append('Session History')
    if current_page == '/userInformation':
        expand_nodes.append('Patient Information')

    tree_data = [{
        'id': 'Patient Records',
        'label': 'Patient Records',
        'children': [
            {
                'id': 'Patient Information',
                'label': bold('User Information') if current_page == '/userInformation' else 'Patient Information',
                'children': patient_nodes,
            },
            {
                'id': 'Session History',
                'label': bold('Session History') if current_page == '/sessionHistory' else 'Session History',
                'children': session_date_nodes,
            },
        ],
    }]

    ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(expand_nodes)


@ui.page('/user')
def main():
    app.storage.user['current_page'] = '/user'
    patient = get_patient(patient_id=app.storage.user["selected_patient"], token=app.storage.user["token"])
    utilities.header()
    ui.page_title('SocketFit Dashboard')

    with ui.row().classes('w-full'):
        ui.label('User').classes('text-xl font-semibold ml-[21%]')

    with ui.row().classes('w-full h-[800px]'):
        # remove session_tree() for now if it caused the timestamp error
        #with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            #utilities.session_tree()

        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]'):
            if not patient:
                ui.label('No patients loaded yet.').classes('p-4 text-gray-600')
                return

            # user information boxes
            with ui.row():
                with ui.row().classes('w-2/5 items-start'):
                    with ui.input(label='First Name', value=(patient.first_name)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Last Name', value=(patient.last_name)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Weight (kg)', value=(patient.weight)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Height (cm)', value=(patient.height)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Amputation Type', value=(patient.amputation_type)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Prosthetic Type', value=(patient.prosthetic_type)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Email', value=(patient.email)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Patient ID', value=(patient.patient_id)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Clinician ID', value=(patient.clinician_id)).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('person').classes('text-black text-3xl h-full flex items-center mr-2')
                ui.space()
                # additional notes section
                with ui.column().classes('w-2/5'):
                    ui.label("Additional Notes").classes('text-xl self-start')
                    ui.textarea(placeholder='Enter Notes Here').classes('h-full w-full border rounded-md border-[#3545FF]')

ui.run(fastapi_docs=True, storage_secret="HELPPP")