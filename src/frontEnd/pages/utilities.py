from nicegui import ui, app
import ActivityPage
import Homepage
from collections import OrderedDict
from datetime import datetime
import UserInformation


# making text in tree bold
def bold(text):
    return ''.join(
        chr(ord(c) + 0x1D400 - ord('A')) if 'A' <= c <= 'Z' else
        chr(ord(c) + 0x1D41A - ord('a')) if 'a' <= c <= 'z' else
        chr(ord(c) + 0x1D7CE - ord('0')) if '0' <= c <= '9' else
        c for c in text
    )

# making sidebar tree for sessions
def session_tree(): 
            current_page = app.storage.user.get('current_page', '')
            selected_patient_index = app.storage.user.get('selected_patient_index')
            selected_session_date = app.storage.user.get('selected_session_date')
            session_date_nodes = []
            seen_dates = OrderedDict()
            expand_nodes = ['User Records']
            if current_page == '/sessionHistory':
                 expand_nodes.append('Session History')
            elif current_page != '/sesionHistory' and current_page != '/activity':
                 if 'Session History' in expand_nodes:
                    expand_nodes.remove('Session History')

            for activity in app.storage.user.get('activityList', []):
                dt_str1 = activity.start_time
                dt_format = "%d-%b-%Y %H:%M:%S"
                dt1 = datetime.strptime(dt_str1, dt_format)
                date_label = dt1.strftime("%d %b %Y")

                if date_label not in seen_dates:
                    label = bold(date_label) if selected_session_date == date_label else date_label
                    seen_dates[date_label] = {
                        'id': f'{date_label}',
                        'label': label
                    }
            session_date_nodes = list(seen_dates.values())
            patient_nodes = []
            for i, patient in enumerate(app.storage.user.get('patients', [])):
                base = f'User {chr(65+i)}'
                label = bold(base) if selected_patient_index == i else base
                patient_nodes.append({
                'id': f'patient-{i}',
                'label': label
        })
                expand_nodes = ['User Records']
                if current_page == '/sessionHistory':
                    expand_nodes.append('Session History')
                if current_page == '/userInformation':
                    expand_nodes.append('User Information')

            tree_data = [
                {
                    'id': 'User Records',
                    'label': 'User Records',
                    'children': [
                        {
                            'id': 'User Information',
                            'label': bold('User Information') if current_page == '/userInformation' else 'User Information',
                            'children': patient_nodes
                        },
                        {
                            'id': 'Session History',
                            'label': bold('Session History') if current_page == '/sessionHistory' else 'Session History',
                            'children': session_date_nodes
                        }
                    ]
                }
            ]

            tree = ui.tree(
                tree_data, 
                label_key='label', 
                on_select=on_tree_select
            ).expand(expand_nodes)

def on_tree_select(e):
    label_to_path = {
        'User Records': '/main',
        'User Information': '/userInformation',
        'Session History': '/sessionHistory',
    }

    selected = e.value

    # handle patient leaf clicks
    if isinstance(selected, str) and selected.startswith('patient-'):
        idx = int(selected.split('-')[-1])
        app.storage.user['selected_patient_index'] = idx
        selected_patient = app.storage.user.get('patients', [])[idx]
        app.storage.user['patient'] = selected_patient
        UserInformation.navigatePatient(selected_patient)
        return

    # handle session-date leaf clicks
    for activity in app.storage.user.get('activityList', []):
        dt = datetime.strptime(activity.start_time, "%d-%b-%Y %H:%M:%S")
        if dt.strftime("%d %b %Y") == selected:
            app.storage.user['selected_session_date'] = selected  # remember which date is active
            app.storage.user['activity'] = activity
            ActivityPage.navigateActivity()
            return
    

    # handle section nodes
    if selected in label_to_path:
        if selected == 'Session History':
            app.storage.user['filter_date'] = None
            app.storage.user['selected_session_date'] = None
        ui.navigate.to(label_to_path[selected])

# making sidebar tree for patients
def patients_tree():
    current_page = app.storage.user.get('current_page', '')
    # FOR NOW PATIENTS NODES HAVE TITLES SUCH AS USER A,B....... LATER CAN BE CHANGED WHEN WE HAVE NAMES
    patient_nodes = []
    for i, patient in enumerate(app.storage.user.get('patients', [])):
        patient_nodes.append({
            'id': f'patient-{i}',
            'label': f'User {chr(65 + i)}'
        })

    tree_data = [
        {
            'id': 'User Records',
            'label': bold('User Records') if current_page == '/main' else 'User Records',
            'children': patient_nodes
        }
    ]

    ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(['User Records'])

# making standard header
def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.link(target='/login'):
            ui.image('src\\frontEnd\\assets\\SocketFitDashboard.png').classes('h-[40px] w-[140px]')