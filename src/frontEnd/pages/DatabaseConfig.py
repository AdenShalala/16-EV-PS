from nicegui import ui
import utilities
# keep writefromfile import
import WriteFromFile
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backEnd', 'databases', 'SQL'))
from SQL_Setup import database_connect # pyright: ignore[reportMissingImports]

# state variable
selected_db_type = 'MySQL'  # default

def header():
    utilities.header()

@ui.page('/config')
def config():
    ui.page_title("SocketFit Dashboard")
    header()

    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]'):
            utilities._clinicians_tree()
            ui.link('Database Configuration', '/config').style('color: black; text-decoration: none; padding: 05px;')
            ui.link('Write from file', '/writeFile').style(f'color: black; text-decoration: none; padding: 05px;')
        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            with ui.row().classes('items-center gap-4'):
                ui.select(
                    label='Database Choice',
                    options=['MySQL', 'MongoDB', 'InfluxDB'],
                    value='MySQL',
                    #on_change=lambda e: show_inputs_based_on_db(e.value)
                ).classes('rounded-md border border-[#2C25B2] px-4 py-2 text-md')
            # with ui.row().classes('items-center gap-4'):
                # ui.button(
                #     'Advanced Database Configuration',
                #     on_click=lambda: ui.navigate.to('/advanced-config'), color="#FFB030"
                # ).classes('bg-orange-400 text-white mt-4 px-3 py-2 rounded-md text-sm')
            placeholder_column_inputs(main)
            

def placeholder_column_inputs(container):
    """Draw initial 4 placeholder inputs inside a container"""
    with container:
        host_input = ui.input(placeholder='HOST').classes('border rounded-md border-[#3545FF]')
        user_input = ui.input(placeholder='USER').classes('border rounded-md border-[#3545FF]')
        password_input = ui.input(placeholder='PASSWORD').classes('border rounded-md border-[#3545FF]')
        database_input = ui.input(placeholder='DATABASE').classes('border rounded-md border-[#3545FF]')
        port_input = ui.input(placeholder='PORT').classes('border rounded-md border-[#3545FF]')
        ui.button(
                    'Submit Details and Initialise Database',
                    on_click=lambda: write_new_env(host_input.value, user_input.value, password_input.value, database_input.value, port_input.value), color="#FFB030"
                ).classes('bg-orange-400 text-white mt-4 px-3 py-2 rounded-md text-sm')


def navigateConfig():
    ui.navigate.to('/config')

def show_inputs_based_on_db(db_type):
    """Update inputs dynamically based on selected DB"""
    ui.clean()
    config()

def write_new_env(host, user, passw, db, port):
    env = (
        f"MYSQL_HOST='{host}'\n"
        f"MYSQL_USER='{user}'\n"
        f"MYSQL_PASSWORD='{passw}'\n"
        f"MYSQL_DATABASE='{db}'\n"
        f"MYSQL_PORT='{port}'\n"
    )
    with open('.env', 'w') as f:
        f.write(env)
    ui.notify(" .env file saved successfully!")

    database_connect()
