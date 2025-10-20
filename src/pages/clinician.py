from nicegui import ui, app
import pages.utilities as utilities
import api
from schema import Clinician

def create() -> None:
    @ui.page('/admin/clinician')
    def clinician():
        app.storage.user['current_page'] = '/admin/clinician'
        clinician: Clinician = api.get_clinician(app.storage.user.get("selected_clinician"), app.storage.user.get("token"))
        utilities.header()
        ui.page_title('SocketFit Admin — Clinician Information')

        with ui.row().classes('w-full'):
            ui.label('Admin').classes('text-xl font-semibold ml-[21%]')

        with ui.row().classes('w-full h-[800px]'):
            with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
                utilities.clinicians_tree()

            with ui.card().classes('w-3/4 h-full border border-[#2C25B2]'):
                if not clinician:
                    ui.label('No clinicians loaded yet.').classes('p-4 text-gray-600')
                    return

                with ui.row():
                    with ui.row().classes('w-2/5 items-start'):
                        with ui.input(label='First Name', value=clinician.first_name) \
                            .classes('w-full border rounded-md border-[#3545FF] p-1'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')

                        with ui.input(label='Last Name', value=clinician.last_name) \
                            .classes('w-full border rounded-md border-[#3545FF] p-1'):
                            ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')

                        with ui.input(label='Email', value=clinician.email) \
                            .classes('w-full border rounded-md border-[#3545FF] p-1'):
                            ui.icon('mail').classes('text-black text-3xl h-full flex items-center mr-2')

                        with ui.input(label='Clinician ID', value=clinician.clinician_id) \
                            .classes('w-full border rounded-md border-[#3545FF] p-1'):
                            ui.icon('person').classes('text-black text-3xl h-full flex items-center mr-2')

                    ui.space()

                    with ui.column().classes('w-2/5'):
                        ui.label("Notes").classes('text-xl self-start')
                        ui.textarea(placeholder='Enter Notes Here') \
                        .classes('h-full w-full border rounded-md border-[#3545FF]')

