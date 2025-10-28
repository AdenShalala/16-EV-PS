from nicegui import ui, app
import pages.utilities as utilities
import api
from functools import partial

# navigating to dashboard page
def navigate_dashboard(patient):
    app.storage.user['selected_patient'] = patient.patient_id
    ui.navigate.to("/dashboard")

# navigating to a selected patient
def navigate_patient(patient):
    app.storage.user['selected_patient'] = patient.patient_id
    ui.navigate.to("/patient")

# sorting patients alphabetically
def sort(e):
  return f'{e.first_name} {e.last_name}'

def create() -> None:
    # root page
    @ui.page('/')
    def root():
        # setting current page in storage
        app.storage.user['current_page'] = '/'

        # getting patients
        patients = api.get_patients(app.storage.user.get("token"))

        # adding in title header and sidebar
        ui.page_title("SocketFit Dashboard")
        utilities.header()
        left_drawer = utilities.sidebar()
        
        options = []

        patients.sort(key=sort)

        for patient in patients:
            options.append(f'{patient.first_name} {patient.last_name}')

        # adding in sidebar arrow and patient search filter
        with ui.row().classes('w-full h-full justify-between'):
            arrow = utilities.arrow(left_drawer)
            patient_search = ui.input(placeholder='Search', autocomplete=options).classes('border-[#2C25B2] border rounded-md p-1').on_value_change(lambda: patients_display())

        patients_container = ui.row().classes('w-full h-full')
        # displaying patients
        def patients_display():
            filtered_patients = patients
            if patient_search.value:
                filtered_patients = [patient for patient in patients if patient_search.value.lower() in (patient.first_name + ' ' + patient.last_name).lower()]
            patients_container.clear()
            with patients_container:
                for patient in filtered_patients:
                    with ui.card().classes('w-full h-full bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2] no-shadow'):
                        with ui.row().classes(replace='items-center justify-between w-full '):
                            with ui.row().classes('w-full flex justify-between'):
                                with ui.row().classes('w-full justify-between items-center'):
                                    with ui.button().classes('px-0').props('flat no-caps color=black align="left"').on_click(partial(navigate_patient, patient)):
                                        ui.icon('sym_o_info_i').classes('text-white bg-[#FFB030] rounded-full mr-2 shadow-md').props('round')
                                        ui.label(f"{patient.first_name} {patient.last_name}").classes('font-bold text-2xl dark:text-white')

                                    
                                    ui.button(icon='arrow_forward_ios', color='#FFB030').classes('text-white').on_click(partial(navigate_dashboard, patient))
                            with ui.row().classes('items-center gap-2 w-full'):
                                with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                                    ui.label(patient.email).classes('text-xs text-grey')
                                    ui.label(patient.patient_id).classes('text-xs text-grey')
                        ui.separator()
                        with ui.row().classes('items-center w-full -my-2'):
                            with ui.grid(columns='auto auto auto auto auto auto').classes('w-full'):
                                ui.label('Height').classes('font-bold')
                                ui.label('Weight').classes('font-bold')
                                ui.label('Amputation Type').classes('font-bold')
                                ui.label('Socket Type').classes('font-bold')
                                ui.label('Amputation Date').classes('font-bold')
                                ui.label('Prosthetic Fitting Date').classes('font-bold')
                                ui.label(patient.height + "cm")
                                ui.label(patient.weight + "kg")
                                ui.label(patient.amputation_type)
                                ui.label(patient.socket_type)        
                                ui.label(patient.amputation_date.strftime("%Y-%m-%d"))
                                ui.label(patient.prosthetic_fitting_date.strftime("%Y-%m-%d"))

        patients_display()