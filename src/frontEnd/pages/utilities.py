
from nicegui import ui, app
import ActivityPage
import Homepage
from collections import OrderedDict
from datetime import datetime, timezone
import UserInformation


def bold(text):
    return ''.join(
        chr(ord(c) + 0x1D400 - ord('A')) if 'A' <= c <= 'Z' else
        chr(ord(c) + 0x1D41A - ord('a')) if 'a' <= c <= 'z' else
        chr(ord(c) + 0x1D7CE - ord('0')) if '0' <= c <= '9' else
        c for c in text
    )

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

def on_tree_select(e):
    label_to_path = {
        'Patient Records': '/main',
        'Patient Information': '/userInformation',
        'Session History': '/sessionHistory',
    }
    selected = e.value

    if isinstance(selected, str) and selected.startswith('patient-'):
        idx = int(selected.split('-')[-1])
        app.storage.user['selected_patient_index'] = idx
        selected_patient = app.storage.user.get('patients', [])[idx]
        app.storage.user['patient'] = selected_patient
        UserInformation.navigatePatient(selected_patient)
        return

    # Check if selected is an activity_id
    for activity in app.storage.user.get('activityList', []):
        activity_id = _get(activity, 'activity_id')
        if activity_id == selected:
            app.storage.user['selected_session_date'] = selected  # Store the activity_id
            app.storage.user['activity'] = activity
            ActivityPage.navigateActivity()
            return

    if selected in label_to_path:
        if selected == 'Session History':
            app.storage.user['filter_date'] = None
            app.storage.user['selected_session_date'] = None
        ui.navigate.to(label_to_path[selected])

def patients_tree():
    current_page = app.storage.user.get('current_page', '')
    patient_nodes = []
    for i, patient in enumerate(app.storage.user.get('patients', [])):
        full_name = f"{patient.first_name} {patient.last_name}"
        patient_nodes.append({
            'id': f'patient-{i}',
            'label': full_name
        })
    tree_data = [{
        'id': 'Patient Records',
        'label': bold('Patient Records') if current_page == '/main' else 'Patient Records',
        'children': patient_nodes,
    }]
    ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(['Patient Records'])

def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.link(target='/login'):
            ui.image('src\\frontEnd\\assets\\SocketFitDashboard.png').classes('h-[40px] w-[140px]')
