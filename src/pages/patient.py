from nicegui import ui, app
import api
import pages.utilities as utilities


def create() -> None:
    @ui.page('/patient')
    def patient():
        app.storage.user['current_page'] = '/patient'
        patient = api.get_patient(patient_id=app.storage.user.get("selected_patient"), token=app.storage.user.get("token"))
        utilities.header()
        utilities.sidebar()
        ui.page_title('SocketFit Dashboard')


        with ui.row().classes(' w-full flex justify-center'):
            with ui.card().classes('w-2/5 justify-center items-center bg-[#F5F5F5] dark:bg-[#0A0A0A] border border-[#2C25B2]'):
                if not patient:
                    ui.label('No patients loaded yet.').classes('p-4 text-gray-600')
                    return

                # user information boxes
                with ui.row().classes():
                    with ui.grid(rows=2, columns=1).classes(replace=''):
                        ui.label(f"{patient.first_name} {patient.last_name}").classes('font-bold text-xl dark:text-white')
                        ui.label(patient.patient_id).classes('text-xs text-grey')


                    with ui.row().classes('w-full items-start'):
                        with ui.input(label='First Name', value=patient.first_name).classes('w-full border rounded-md border-[#3545FF]') as first_name:
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Last Name', value=patient.last_name).classes('w-full border rounded-md border-[#3545FF]') as last_name:
                            last_name.disable()
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Email', value=patient.email).classes('w-full border rounded-md border-[#3545FF]') as email:
                            email.disable()
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Weight (kg)', value=patient.weight).classes('w-full border rounded-md border-[#3545FF]') as weight:
                            weight.disable()
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Height (cm)', value=patient.height).classes('w-full border rounded-md border-[#3545FF]') as height:
                            height.disable()
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Amputation Type', value=patient.amputation_type).classes('w-full border rounded-md border-[#3545FF]') as amputation:
                            amputation.disable()
                            ui.button(icon="edit").classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                        with ui.input(label='Prosthetic Type', value=patient.prosthetic_type).classes('w-full border rounded-md border-[#3545FF]') as prosthetic:
                            prosthetic.disable()
                            ui.button(icon="edit", on_click=lambda: ui.notify('You clicked me!')).classes('h-full flex items-center mr-2').props('flat no-caps color=black')
                            
                    ui.space()
