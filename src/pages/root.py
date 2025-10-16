from nicegui import ui, app
import pages.utilities as utilities
import api
from functools import partial

def patientpass(patient):
    app.storage.user['selected_patient'] = patient.patient_id
    ui.navigate.to("/activity")

def create() -> None:
    @ui.page('/')
    def root():
        def select(e):
            selected = e.value

            if isinstance(selected, str) and selected.startswith('patient.'):
                id = selected.split('.')[1]
                app.storage.user["selected_patient"] = id
                return

        def navigatePatient(patient):
            app.storage.user['selected_patient'] = patient.patient_id
            ui.navigate.to('/patient')

        app.storage.user['current_page'] = '/'

        patients = api.get_patients(app.storage.user.get("token"))

        if app.storage.user.get('darkbool') == True:
            dark = ui.dark_mode()
            dark.enable()

        ui.page_title("SocketFit Dashboard")
        # genderList = ['All', 'Male', 'Female', 'Prefer not to say']
        # amputationTypeList = ['All', 'Above Knee', 'Below Knee', 'Above Elbow', 'Below Elbow']

        utilities.header()
        utilities.sidebar()

        # amputationTypeList = ['All']

        with ui.row().classes('w-full h-full'):
            for patient in patients:
                with ui.card().classes('w-full h-full bg-[#F5F5F5] dark:bg-[#0A0A0A]'):
                    with ui.row().classes(replace='items-center justify-between w-full '):
                        with ui.row().classes('w-full flex justify-between'):
                            with ui.button().classes('px-0').props('flat no-caps color=black align="left"').on_click(partial(patientpass, patient)):
                                ui.label(f"{patient.first_name} {patient.last_name}").classes('font-bold text-2xl dark:text-white')

                            ui.button(icon='arrow_forward_ios', color='#FFB030').props().classes('text-white').on_click(partial(patientpass, patient))
                        with ui.row().classes('items-center gap-2 w-full'):
                            with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                                ui.label(patient.email).classes('text-xs text-grey')
                                ui.label(patient.patient_id).classes('text-xs text-grey')

                 #           ui.button(icon='arrow_forward_ios', color='#FFB030').props('round').classes('text-white').
                    ui.separator()
                    with ui.row().classes('items-center w-full'):
                        with ui.grid(columns='auto auto auto auto').classes('w-full'):
                            ui.label('Height').classes('font-bold')
                            ui.label('Weight').classes('font-bold')
                            ui.label('Amputation Type').classes('font-bold')
                            ui.label('Prosthetic Type').classes('font-bold')
                            

                            ui.label(patient.height + "cm")
                            ui.label(patient.weight + "kg")
                            ui.label(patient.amputation_type)
                            ui.label(patient.prosthetic_type)