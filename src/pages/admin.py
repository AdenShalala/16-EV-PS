
from nicegui import ui, app
import os, sys
#import ClinicianInformation
import pages.utilities as utilities
import api
from schema import Clinician

# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backEnd', 'databases', 'SQL'))
# import SQL_read   

def _select_and_go(clinician: Clinician):
    app.storage.user['selected_clinician'] = clinician.clinician_id
    ui.navigate.to('/admin/clinician')

def _render_cards(clinicians: list[Clinician], mount):
    mount.clear()
    with mount:
        with ui.grid(columns=4).classes('w-full gap-6'):
            for clinician in clinicians:
                full_name = f'{clinician.first_name} {clinician.last_name}'.strip() or 'Unnamed'
                with ui.card().classes(
                    'h-[150px] w-[160px] border border-[#2C25B2] cursor-pointer'
                ).on('click', lambda _, cc=clinician: _select_and_go(cc)):
                    ui.label(full_name).classes('text-xl')

def create() -> None:
    @ui.page('/admin')
    def admin():
        app.storage.user['current_page'] = '/admin'
        ui.page_title('SocketFit Admin')
        utilities.header()

        with ui.row().classes('w-full'):
            with ui.card().classes('w-1/5 border border-[#2C25B2]'):
                # SideTree need some stuff to be fixed to be consistent
                utilities.clinicians_tree()

            with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2]'):
                with ui.column().classes('w-full p-4 gap-4'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('Select Clinician to View Information').classes('text-2xl font-bold')

                    cards_container = ui.column()
                    clinicians = api.get_clinicians(token=app.storage.user.get("token"))
                    # app.storage.user['clinicians'] = clinicians
                    if not clinicians:
                        ui.label('No clinicians found.').classes('text-gray-600')
                    else:
                        _render_cards(clinicians, cards_container)


