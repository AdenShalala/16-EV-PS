
from nicegui import ui, app
import os, sys
import ClinicianInformation
import utilities


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backEnd', 'databases', 'SQL'))
import SQL_read   


import utilities
def header():
    utilities.header()


def navigateAdminHome():
    ui.navigate.to('/admin/home')


def _full_name(c):
    fn = (c.get('first_name') or '').strip()
    ln = (c.get('last_name') or '').strip()
    return f'{fn} {ln}'.strip() or 'Unnamed'

def _select_and_go(c):
    app.storage.user['clinician'] = c
    ui.navigate.to('/admin/clinicianInfo')

def _render_cards(c_list, mount):
    mount.clear()
    with mount:
        with ui.grid(columns=4).classes('w-full gap-6'):
            for c in c_list:
                full_name = _full_name(c)
                with ui.card().classes(
                    'h-[150px] w-[160px] border border-[#2C25B2] cursor-pointer'
                ).on('click', lambda _, cc=c: _select_and_go(cc)):
                    ui.label(full_name).classes('text-xl')

@ui.page('/admin/home')
def admin_home():
    app.storage.user['current_page'] = '/admin/home'
    ui.page_title('SocketFit Admin')
    header()

    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]'):
            # SideTree need some stuff to be fixed to be consistent
            utilities._clinicians_tree()
            ui.link('Database Configuration', '/config').style('color: black; text-decoration: none; padding: 05px;')
            ui.link('Write from file', '/writeFile').style(f'color: black; text-decoration: none; padding: 05px;')

        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2]') as main:
            with ui.column().classes('w-full p-4 gap-4'):
                with ui.row().classes('w-full justify-between items-center'):
                    ui.label('Select Clinician to View Information').classes('text-2xl font-bold')

                cards_container = ui.column()
                clinicians = SQL_read.list_all_clinicians()
                app.storage.user['clinicians'] = clinicians
                if not clinicians:
                    ui.label('No clinicians found.').classes('text-gray-600')
                else:
                    _render_cards(clinicians, cards_container)


