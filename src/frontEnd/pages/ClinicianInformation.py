from nicegui import ui, app
import utilities

def header():
    utilities.header()

def _get(obj, key, default=""):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)

def _ensure_current_clinician():
    c = app.storage.user.get('clinician')
    if c:
        return c
    clinicians = app.storage.user.get('clinicians') or []
    if not clinicians:
        return None
    app.storage.user['selected_clinician_index'] = 0
    app.storage.user['clinician'] = clinicians[0]
    return clinicians[0]

def _clinicians_tree():
    clinicians = app.storage.user.get('clinicians') or []
    for c in clinicians:
        name = f"{_get(c, 'first_name')} {_get(c, 'last_name')}".strip() or 'Unnamed'
        ui.link(name, '#').on('click', lambda _=None, cc=c: navigateClinician(cc)) \
                               .style('color: black; text-decoration: none;')

@ui.page('/admin/clinicianInfo')
def main():
    app.storage.user['current_page'] = '/admin/clinicianInfo'
    clinician = _ensure_current_clinician()
    header()
    ui.page_title('SocketFit Admin — Clinician Information')

    with ui.row().classes('w-full'):
        ui.label('Admin').classes('text-xl font-semibold ml-[21%]')

    with ui.row().classes('w-full h-[800px]'):
        # LEFT: sidetree (clinicians list)
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]'):
            _clinicians_tree()
            ui.link('Database Configuration', '/config').style('color: black; text-decoration: none;')
            ui.link('Write from file', '/writeFile').style('color: black; text-decoration: none;')

        # RIGHT: clinician info panel
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]'):
            if not clinician:
                ui.label('No clinicians loaded yet.').classes('p-4 text-gray-600')
                return

            with ui.row():
                with ui.row().classes('w-2/5 items-start'):
                    with ui.input(label='First Name', value=_get(clinician, 'first_name')) \
                        .classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')

                    with ui.input(label='Last Name', value=_get(clinician, 'last_name')) \
                        .classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('badge').classes('text-black text-3xl h-full flex items-center mr-2')

                    with ui.input(label='Email', value=_get(clinician, 'email')) \
                        .classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('mail').classes('text-black text-3xl h-full flex items-center mr-2')

                    with ui.input(label='Clinician ID', value=_get(clinician, 'clinician_id')) \
                        .classes('w-full border rounded-md border-[#3545FF]'):
                        ui.icon('person').classes('text-black text-3xl h-full flex items-center mr-2')

                ui.space()

                with ui.column().classes('w-2/5'):
                    ui.label("Notes").classes('text-xl self-start')
                    ui.textarea(placeholder='Enter Notes Here') \
                      .classes('h-full w-full border rounded-md border-[#3545FF]')

def navigate():
    ui.navigate.to('/admin/clinicianInfo')

def navigateClinician(clinician):
    app.storage.user['clinician'] = clinician
    ui.navigate.to('/admin/clinicianInfo')
