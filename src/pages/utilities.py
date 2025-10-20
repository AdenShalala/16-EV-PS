from nicegui import ui, app
from collections import OrderedDict
from datetime import datetime, timezone
import api


def toggle_sidebar(left_drawer, arrow):
    if left_drawer.value:
        arrow.icon='arrow_forward'
    else:
        arrow.icon='arrow_back'
    left_drawer.toggle()

def navigatePatient():
    patients = api.get_patients(app.storage.user.get("token"))
    if app.storage.user.get('selected_patient') == None or app.storage.user.get('selected_patient') == '' or app.storage.user.get('selected_patient') == ' ':
        app.storage.user['selected_patient'] = patients[0].patient_id
    ui.navigate.to('/activity')

def toggle_dark_mode(value, button):
    dark = ui.dark_mode()
    if value == True:
        app.storage.user['dark_mode'] = False
        dark.disable()
        button.name='dark_mode'
    else:
        app.storage.user['dark_mode'] = True
        dark.enable()
        button.name='light_mode'

def sidebar():
    with ui.left_drawer(fixed=False, elevated=True,).props('width=200') as left_drawer:
        patients = ui.button('Patients', icon='groups', on_click=lambda: ui.navigate.to('/')).props('flat no-caps align=left').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0 !text-gray-600 dark:!text-gray-400'
        )
        dashboard = ui.button('Dashboard', icon='dashboard', on_click=lambda: navigatePatient()).props('flat no-caps align=left').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0 !text-gray-600 dark:!text-gray-400'
        )
        account = ui.button('Account', icon='account_circle').props('flat no-caps color=grey-8 align=left').classes(
            'w-full justify-start rounded-none hover:bg-primary/10 transition-colors text-base m-0 !text-gray-600 dark:!text-gray-400'
        )
    arrow = ui.button(color='white', on_click=lambda: toggle_sidebar(left_drawer, arrow)).classes('p-[-10px] ml-[-15px] z-100 !text-black dark:!bg-[#1d1d1d] dark:!text-white')
    if left_drawer.value:
        arrow.icon='arrow_forward'
    else:
        arrow.icon='arrow_back'
    if app.storage.user.get('current_page') == '/':
        patients.classes(remove='!text-gray-600 dark:!text-gray-400', add='!text-blue-700')
    elif app.storage.user['current_page'] == '/activity':
        dashboard.classes(remove='!text-gray-600 dark:!text-gray-400', add='!text-blue-700')

def header():
    if not "dark_mode" in app.storage.user:
        dark = ui.dark_mode()
        app.storage.user["dark_mode"] = dark.value

    with ui.header(elevated=True).classes('bg-[#ffffff] dark:bg-[#1d1d1d]'):
        with ui.row().classes('w-full justify-between items-center px-2'):
            with ui.row().classes('items-center gap-4'):
                with ui.link(target='/'):
                    ui.image('/assets/dashboard.png').classes('h-[40px] w-[150px]')
            def logout():
                api.logout(token=app.storage.user.get("token"))
                app.storage.user.clear()
                ui.navigate.to('/login')

            with ui.row().classes('items-center gap-4'):

                dark_button = ui.icon('dark_mode').on('click', lambda: toggle_dark_mode(app.storage.user.get("dark_mode"), dark_button)).classes('!text-gray-600 dark:!text-gray-400 cursor-pointer text-3xl')
                toggle_dark_mode(not app.storage.user["dark_mode"], dark_button)
                if app.storage.user.get('dark_mode') == True:
                    dark_button.name='light_mode'
                elif app.storage.user.get('dark_mode') == False:
                    dark_button.name='dark_mode'
                ui.button('Logout', on_click=logout, color='#FFB030').classes(
                'text-white rounded-md px-6 py-2')



def normalize_to_str(value: str | int | float | datetime) -> str:
    """Return time as 'dd-Mon-YYYY HH:MM:SS' string, no tzinfo."""
    if value is None:
        return None

    # if it's already a datetime
    if isinstance(value, datetime):
        return value.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a unix timestamp
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        dt = datetime.fromtimestamp(int(value))
        return dt.strftime("%d-%b-%Y %H:%M:%S")

    # if it's a string datetime
    value = str(value).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S%z",   # 2023-08-28 12:33:20+00:00
        "%Y-%m-%d %H:%M:%S",     # 2023-08-28 12:33:20
        "%Y-%m-%dT%H:%M:%S",     # 2023-08-28T12:33:20
        "%d-%b-%Y %H:%M:%S",     # 28-Aug-2023 12:33:20
        "%d %b %Y",              # 28 Aug 2023
        "%Y-%m-%d"               # 2023-08-28
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%d-%b-%Y %H:%M:%S")
        except ValueError:
            continue

    raise ValueError(f"Unsupported datetime format: {value!r}")
