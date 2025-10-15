from nicegui import ui, app
from collections import OrderedDict
from datetime import datetime, timezone
import api

def header():
    with ui.left_drawer(fixed=False, elevated=True).props('width=250') as left_drawer:
        patients = ui.button('Patients', icon='groups', on_click=lambda: ui.navigate.to('/')).props('flat no-caps color=grey-8').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0'
        )
        dashboard = ui.button('Dashboard', icon='dashboard').props('flat no-caps color=grey-8').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0'
        )
        account = ui.button('Account', icon='account_circle').props('flat no-caps color=grey-8').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0'
        )
    if app.storage.user.get('current_page') == '/':
        patients.props('color=blue-700')
    # elif app.storage.user.get('current_page') == '/':
    with ui.header(elevated=True).style('background-color: #FFFFFF'):
        with ui.row().classes('w-full justify-between items-center px-2'):
            with ui.row().classes('items-center gap-4'):
                with ui.link(target='/'):
                    ui.image('/assets/dashboard.png').classes('h-[40px] w-[150px]')
                ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=black')
            def logout():
                app.storage.user.clear()
                ui.navigate.to('/login')

            ui.button('Logout', on_click=logout, color='#FFB030').classes(
            'text-white rounded-md px-6 py-2')

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
    selected_patient = app.storage.user.get('selected_patient')
    if current_page == '/activity':
        activity = api.get_activity(app.storage.user.get("selected_patient"), app.storage.user.get("selected_activity"), app.storage.user.get("token"))
        selected_session_date = activity.activity_id
    else: 
        selected_session_date = None

    seen_dates = OrderedDict()
    for activity in api.get_activities(app.storage.user.get("selected_patient"), app.storage.user.get("token")):
        dt1 = _to_dt(activity.start_time)
        date_label = _date_label(dt1)
        
        if activity.activity_id not in seen_dates:
            # Combine date and activity type first, then apply bold to the whole thing
            full_label = date_label + " " + activity.activity_type
            label = full_label
            seen_dates[activity.activity_id] = {'id': activity.activity_id, 'label': label}

    session_date_nodes = list(seen_dates.values())

    patient_nodes = []
    for patient in api.get_patients(token=app.storage.user.get("token")):
        full_name = f"{patient.first_name} {patient.last_name}"
        patient_nodes.append({
            'id': f'patient.{patient.patient_id}',
            'label': full_name
        })

    expand_nodes = ['Patient Records']
    if current_page == '/patient/session' or current_page == '/activity':
        expand_nodes.append('Session History')
    if current_page == '/patient':
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

def normalize_to_str(value: str | int | float | datetime) -> str:
    """Return time as 'dd-Mon-YYYY HH:MM:SS' string, no tzinfo."""
    if value is None:
        return None

    # if it's already a datetime
    if isinstance(value, datetime):
        return value.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a unix timestamp
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        dt = datetime.fromtimestamp(int(value))
        return dt.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a string datetime
    value = str(value).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S%z",   # 2023-08-28 12:33:20+00:00
        "%Y-%m-%d %H:%M:%S",     # 2023-08-28 12:33:20
        "%Y-%m-%dT%H:%M:%S",     # 2023-08-28T12:33:20
        "%d-%b-%Y %H:%M:%S",     # 28-Aug-2023 12:33:20
        "%d %b %Y",              # 28 Aug 2023
        "%Y-%m-%d"               # 2023-08-28
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%d-%b-%Y %H:%M:%S")
        except ValueError:
            continue

    raise ValueError(f"Unsupported datetime format: {value!r}")

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

