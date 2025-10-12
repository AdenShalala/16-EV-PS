from nicegui import app as app, ui
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import api
import pages.utilities as utilities
import session
from collections import OrderedDict

import pages.login as login
import pages.root as root
import pages.admin as admin
import pages.clinician as clinician
import pages.patient as patient

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('token', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path != "/login":
                return RedirectResponse('/login')
        else:
            s = session.validate_session(token=app.storage.user.get('token'))
            
            if s == None:
                app.storage.user.clear()

            if s.account_type == "Admin":
                # redirect if admin
                if not request.url.path.startswith('/_nicegui') and not request.url.path.startswith('/admin'):
                    return RedirectResponse('/admin')
            else:
                # redirect if not admin
                if not request.url.path.startswith('/_nicegui') and request.url.path.startswith('/admin'):
                    return RedirectResponse('/')
                
        return await call_next(request)


app.add_middleware(AuthMiddleware)


login.create()
root.create()
admin.create()
clinician.create()
patient.create()

# def session_tree():
#     current_page = app.storage.user.get('current_page', '')
#     selected_patient_index = app.storage.user.get('selected_patient_index')

#     seen_dates = OrderedDict()
#     for activity in app.storage.user.get('activityList', []):
#         start_raw = activity.start_time
#         dt1 = _to_dt(start_raw)
#         date_label = _date_label(dt1)
        
#         # Use activity_id as the unique key (assuming it exists)
#         activity_id = _get(activity, 'activity_id')  # or however you access the activity ID
        
#         if activity_id not in seen_dates:
#             # Combine date and activity type first, then apply bold to the whole thing
#             full_label = date_label + " " + activity.type
#             label = bold(full_label) if selected_session_date == activity_id else full_label
#             seen_dates[activity_id] = {'id': activity_id, 'label': label}

#     session_date_nodes = list(seen_dates.values())

#     patient_nodes = []
#     for i, patient in enumerate(app.storage.user.get('patients', [])):
#         full_name = f"{patient.first_name} {patient.last_name}"
#         patient_nodes.append({
#             'id': f'patient-{i}',
#             'label': full_name
#         })

#     expand_nodes = ['Patient Records']
#     if current_page == '/sessionHistory' or current_page == '/activity':
#         expand_nodes.append('Session History')
#     if current_page == '/userInformation':
#         expand_nodes.append('Patient Information')

#     tree_data = [{
#         'id': 'Patient Records',
#         'label': 'Patient Records',
#         'children': [
#             {
#                 'id': 'Patient Information',
#                 'label': utilities.bold('User Information') if current_page == '/userInformation' else 'Patient Information',
#                 'children': patient_nodes,
#             },
#             {
#                 'id': 'Session History',
#                 'label': utilities.bold('Session History') if current_page == '/sessionHistory' else 'Session History',
#                 'children': session_date_nodes,
#             },
#         ],
#     }]

#     ui.tree(tree_data, label_key='label', on_select=on_tree_select).expand(expand_nodes)


@ui.page('/user')
def main():
    app.storage.user['current_page'] = '/user'
    patient = api.get_patient(patient_id=app.storage.user["selected_patient"], token=app.storage.user["token"])
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