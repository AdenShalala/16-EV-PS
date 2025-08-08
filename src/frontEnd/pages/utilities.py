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
        c for c in text
    )

# making sidebar tree for sessions
def session_tree(): 
            current_page = app.storage.user.get('current_page', '')
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
                    seen_dates[date_label] = {
                        'id': f'{date_label}',
                        'label': date_label
                    }
            session_date_nodes = list(seen_dates.values())

            tree_data = [
                {
                    'id': 'User Records',
                    'label': 'User Records',
                    'children': [
                        {
                            'id': 'User Information',
                            'label': bold('User Information') if current_page == '/userInformation' else 'User Information'
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

# linking tree to pages
def on_tree_select(e):
    label_to_path = {
        'User Records': '/main',
        'User Information': '/userInformation',
        'Session History': '/sessionHistory',
    }

    selected_label = e.value
    if selected_label in label_to_path:
        if selected_label == 'Session History':
            app.storage.user['filter_date'] = None
        ui.navigate.to(label_to_path[selected_label])
    else:
        # Assume it's a session date like '23 Apr 2025'
        from datetime import datetime
        for activity in app.storage.user.get('activityList', []):
            dt1 = datetime.strptime(activity.start_time, "%d-%b-%Y %H:%M:%S")
            date_label = dt1.strftime("%d %b %Y")
            if date_label == selected_label:
                app.storage.user['activity'] = activity
                ActivityPage.navigateActivity()
                break

# making sidebar tree for patients
def patients_tree():
    # FOR NOW PATIENTS NODES HAVE TITLES SUCH AS USER A,B....... LATER CAN BE CHANGED WHEN WE HAVE NAMES
    patient_nodes = []
    for i, patient in enumerate(app.storage.user.get('patients', [])):
        patient_nodes.append({
            'id': f'patient-{i}',
            'label': f'User {chr(65 + i)}'
        })

    tree_data = [
        {
            'id': 'Patients',
            'label': 'Patients',
            'children': patient_nodes
        }
    ]

    # setting up navigation to user
    def on_patient_select(e):
        selected_id = e.value
        if selected_id.startswith("patient-"):
            index = int(selected_id.replace("patient-", ""))
            selected_patient = app.storage.user.get('patients', [])[index]
            app.storage.user['patient'] = selected_patient
            UserInformation.navigatePatient(selected_patient)

    ui.tree(tree_data, label_key='label', on_select=on_patient_select).expand(['Patients'])

# making standard header
def header():
    with ui.header().style('background-color: #FFFFFF'):
        with ui.link(target='/login'):
            ui.image('src\\frontEnd\\assets\\SocketFitDashboard.png').classes('h-[40px] w-[140px]')