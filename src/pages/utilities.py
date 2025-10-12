from nicegui import ui, app
from collections import OrderedDict
from datetime import datetime, timezone
import api

def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.link(target='/'):
            ui.image('src/assets/dashboard.png').classes('h-[40px] w-[140px]')

def _to_dt(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):                  
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        v = value.strip()
        if v.isdigit():                                  
            return datetime.fromtimestamp(int(v), tz=timezone.utc)
        for fmt in ('%d-%b-%Y %H:%M:%S',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%d'):
            try:
                return datetime.strptime(v, fmt).replace(tzinfo=timezone.utc)
            except ValueError:
                pass
    raise TypeError(f'Unsupported timestamp: {value!r}')

def _get(obj, name, default=None):
    return obj.get(name, default) if isinstance(obj, dict) else getattr(obj, name, default)

def _date_label(dt: datetime) -> str:
    return dt.astimezone().strftime('%d %b %Y')  # e.g., "31 Aug 2023"

# ---------- sidebar tree for sessions & patients ----------
def session_tree():
    current_page = app.storage.user.get('current_page', '')
    selected_patient_index = app.storage.user.get('selected_patient_index')
    if current_page == '/activity':
        selected_session_date = app.storage.user.get('activity').activity_id
    else: 
        selected_session_date = None

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
            label = full_label
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
                'label': 'Patient Information',
                'children': patient_nodes,
            },
            {
                'id': 'Session History',
                'label': 'Session History',
                'children': session_date_nodes,
            },
        ],
    }]

    ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(expand_nodes)

def on_tree_select(e):
    label_to_path = {
        'Patient Records': '/',
        'Patient Information': '/patient',
        'Session History': '/patient/session',
    }

    selected = e.value



    if isinstance(selected, str) and selected.startswith('patient.'):
        id = int(selected.split('.')[-1])
        app.storage.user['selected_patient'] = id
        patient = api.get_patient(patient_id=id, token=app.storage.user.get("token"))

        #app.storage.user['patient'] = selected_patient
        ui.navigate.to('/patient')
        return

    # Check if selected is an activity_id
    # for activity in app.storage.user.get('activityList', []):
    #     activity_id = _get(activity, 'activity_id')
    #     if activity_id == selected:
    #         app.storage.user['selected_session_date'] = selected  # Store the activity_id
    #         app.storage.user['activity'] = activity
    #         #ActivityPage.navigateActivity()
    #         return

    if selected in label_to_path:
        if selected == 'Session History':
            app.storage.user['filter_date'] = None
            app.storage.user['selected_session_date'] = None
        ui.navigate.to(label_to_path[selected])

def patients_tree():
    patients = []
    for patient in api.get_patients(token=app.storage.user.get("token")):
        patients.append({
            'id': f'patient.{patient.patient_id}',
            'label': f"{patient.first_name} {patient.last_name}"
        })
    tree_data = [{
        'id': 'Patient Records',
        'label': 'Patient Records',
        'children': patient,
    }]
    ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(['Patient Records'])

def on_clinician_tree_select(e):
    node_id = e.value
    
    if node_id == "Clinician Records":
        ui.navigate.to('/admin')

    if not node_id or not node_id.startswith('clinician.'):
        return
    id = node_id.split('.', 1)[1]

    app.storage.user['selected_clinician'] = id
    ui.navigate.to('/admin/clinician')

def clinicians_tree():
    current_page = app.storage.user.get('current_page', '')
    clinicians = api.get_clinicians(token=app.storage.user.get("token"))
    clinician_nodes = []
    for clinician in clinicians:
        full_name = f'{clinician.first_name} {clinician.last_name}'.strip() or 'Unnamed'
        clinician_nodes.append({
            'id': f'clinician.{clinician.clinician_id}',
            'label': full_name,
        })

    tree_data = [{
        'id': 'Clinician Records',
        'label': 'Clinician Records',
        'children': clinician_nodes,
    }]

   
    ui.tree(tree_data, label_key='label', on_select=on_clinician_tree_select) \
      .expand(['Clinician Records'] if current_page in {'/admin/clinician', '/admin'} else [])

