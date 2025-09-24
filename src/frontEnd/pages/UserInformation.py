from nicegui import ui, app
import utilities
import SessionHistory

# getting standard header
def header():
    utilities.header()

def _get(p, key, default=""):
    if p is None:
        return default
    if isinstance(p, dict):
        return p.get(key, default)
    return getattr(p, key, default)

def _ensure_current_patient():
    p = app.storage.user.get('patient')
    if p:
        return p
    patients = app.storage.user.get('patients') or []
    if not patients:
        return None
    app.storage.user['selected_patient_index'] = 0
    app.storage.user['patient'] = patients[0]
    return patients[0]

@ui.page('/userInformation')
def main():
    app.storage.user['current_page'] = '/userInformation'
    patient = _ensure_current_patient()
    header()
    ui.page_title('SocketFit Dashboard')

    with ui.row().classes('w-full'):
        ui.label('User').classes('text-xl font-semibold ml-[21%]')

    with ui.row().classes('w-full h-[800px]'):
        # remove session_tree() for now if it caused the timestamp error
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            utilities.session_tree()

        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]'):
            if not patient:
                ui.label('No patients loaded yet.').classes('p-4 text-gray-600')
                return

            # user information boxes
            with ui.row():
                with ui.row().classes('w-2/5 items-start'):
                    with ui.input(label='First Name', value=_get(patient, 'first_name')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Last Name', value=_get(patient, 'last_name')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Weight (kg)', value=str(_get(patient, 'weight', ''))).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Height (cm)', value=str(_get(patient, 'height', ''))).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Amputation Type', value=_get(patient, 'amputation_type')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Prosthetic Type', value=_get(patient, 'prosthetic_type')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Email', value=_get(patient, 'email')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Patient ID', value=_get(patient, 'patient_id')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    with ui.input(label='Clinician ID', value=_get(patient, 'clinician_id')).classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('person').classes('text-black text-3xl h-full flex items-center mr-2')
                ui.space()
                # additional notes section
                with ui.column().classes('w-2/5'):
                    ui.label("Additional Notes").classes('text-xl self-start')
                    ui.textarea(placeholder='Enter Notes Here').classes('h-full w-full border rounded-md border-[#3545FF]')
def navigate():
    ui.navigate.to('/userInformation')

def navigatePatient(patient):
    app.storage.user['patient'] = patient
    ui.navigate.to('/userInformation')
