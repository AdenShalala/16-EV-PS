from nicegui import ui, app
import api
import pages.utilities as utilities


def create() -> None:
    @ui.page('/clinician')
    def clinician():
        app.storage.user['current_page'] = '/clinician'
        clinician = api.get_clinician(clinician_id=app.storage.user.get("selected_clinician"), token=app.storage.user.get("token"))
        utilities.header()
        left_drawer = utilities.admin_sidebar()
        utilities.arrow(left_drawer)
        ui.page_title('SocketFit Admin')


        with ui.row().classes(' w-full flex justify-center'):
            with ui.card().classes('no-shadow w-2/5 justify-center items-center bg-[#F5F5F5] dark:bg-[#1d1d1d] border border-[#2C25B2]'):
                if not clinician:
                    ui.label('Clinician not loaded yet.').classes('p-4 text-gray-600')
                    return

                # user information boxes
                with ui.row().classes('w-full'):
                    with ui.grid(rows=2, columns=1).classes(replace=''):
                        ui.label(f"{clinician.first_name} {clinician.last_name}").classes('font-bold text-xl dark:text-white')
                        ui.label(clinician.clinician_id).classes('text-xs text-grey')


                    with ui.row().classes('w-full items-start'):
                        first_name = ui.input(label='First Name', value=clinician.first_name).classes('w-full border rounded-md border-[#3545FF] p-1')
                        last_name = ui.input(label='Last Name', value=clinician.last_name).classes('w-full border rounded-md border-[#3545FF] p-1')
                        email = ui.input(label='Email', value=clinician.email).classes('w-full border rounded-md border-[#3545FF] p-1')
                            
                        def save():
                            if not utilities.validate_email(email.value):
                                ui.notify('Invalid email', color='red')
                                return
                            
                            if len(first_name.value) < 1 or len(last_name.value) < 1:
                                ui.notify('Invalid name', color='red')
                                return                                
                                                                           

                            clinician.first_name = first_name.value
                            clinician.last_name = last_name.value
                            clinician.email = email.value
                            api.put_clinician(clinician_id=clinician.patient_id, updated_clinician=clinician, token=app.storage.user.get("token"))
                            ui.run_javascript('location.reload();')

                        ui.button('Save', on_click=save, color='#FFB030').classes('text-white rounded-md px-6 py-2')