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
                        first_name = ui.input(label='First Name', value=patient.first_name).classes('w-full border rounded-md border-[#3545FF]')
                        last_name = ui.input(label='Last Name', value=patient.last_name).classes('w-full border rounded-md border-[#3545FF]')
                        email = ui.input(label='Email', value=patient.email).classes('w-full border rounded-md border-[#3545FF]')
                        weight = ui.number(label='Weight (kg)', value=patient.weight).classes('w-full border rounded-md border-[#3545FF]').props('no-spinners')
                        height = ui.number(label='Height (cm)', value=patient.height).classes('w-full border rounded-md border-[#3545FF]').props('no-spinners')
                        amputation = ui.input(label='Amputation Type', value=patient.amputation_type).classes('w-full border rounded-md border-[#3545FF]')
                        prosthetic = ui.input(label='Prosthetic Type', value=patient.prosthetic_type).classes('w-full border rounded-md border-[#3545FF]')
                            
                        def save():
                            if not utilities.validate_email(email.value):
                                ui.notify('Invalid email', color='red')
                                return
                            
                            if len(first_name.value) < 1 or len(last_name.value) < 1:
                                ui.notify('Invalid name', color='red')
                                return                                
                                                             
                            if not height.value:
                                ui.notify('Invalid height', color='red')
                                return   

                            if not weight.value:
                                ui.notify('Invalid height', color='red')
                                return                                                             

                            if int(height.value) < 1 or int(height.value) > 300:
                                ui.notify('Invalid height', color='red')
                                return                                

                            if int(weight.value) < 1 or int(weight.value) > 1000:
                                ui.notify('Invalid weight', color='red')
                                return          

                            if len(amputation.value) < 1:
                                ui.notify('Invalid amputation type', color='red')
                                return      

                            if len(prosthetic.value) < 1:
                                ui.notify('Invalid prosthetic type', color='red')
                                return                                          

                            patient.first_name = first_name.value
                            patient.last_name = last_name.value
                            patient.email = email.value
                            patient.weight = str(weight.value)
                            patient.height = str(height.value)
                            patient.amputation_type = amputation.value
                            patient.prosthetic_type = prosthetic.value
                            api.put_patient(patient_id=patient.patient_id, updated_patient=patient, token=app.storage.user.get("token"))
                            ui.run_javascript('location.reload();')

                        ui.button('Save', on_click=save, color='#FFB030').classes('text-white rounded-md px-6 py-2')