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

        with ui.row().classes('w-full'):
            ui.label('Patient').classes('text-xl font-semibold ml-[21%]')

        with ui.row().classes('w-full h-[800px]'):
            # remove session_tree() for now if it caused the timestamp error
            with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
                utilities.session_tree()

            with ui.card().classes('w-3/4 h-full border border-[#2C25B2]'):
                if not patient:
                    ui.label('No patients loaded yet.').classes('p-4 text-gray-600')
                    return

                # user information boxes
                with ui.row():
                    with ui.row().classes('w-2/5 items-start'):
                        with ui.input(label='First Name', value=patient.first_name).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Last Name', value=patient.last_name).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Weight (kg)', value=patient.weight).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Height (cm)', value=patient.height).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Amputation Type', value=patient.amputation_type).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Prosthetic Type', value=patient.prosthetic_type).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Email', value=patient.email).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                        with ui.input(label='Patient ID', value=patient.patient_id).classes('w-full border rounded-md border-[#3545FF]'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')
                    ui.space()
                    # additional notes section
                    with ui.column().classes('w-2/5'):
                        ui.label("Additional Notes").classes('text-xl self-start')
                        ui.textarea(placeholder='Enter Notes Here').classes('h-full w-full border rounded-md border-[#3545FF]')
