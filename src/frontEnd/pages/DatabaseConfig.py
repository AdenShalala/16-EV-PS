from nicegui import ui
import elements
import WriteFromFile
import os
import sys

# state variable
selected_db_type = 'MySQL'  # default

def header():
    elements.header()

@ui.page('/config')
def config():
    ui.page_title("SocketFit Dashboard")
    header()

    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]'):
            ui.link('Database Configuration', '/config').style('color: black; text-decoration: none;')
            ui.link('Write from file', '/writeFile').style('color: black; text-decoration: none;')
        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            with ui.row().classes('items-center gap-4'):
                ui.select(
                    label='Database Choice',
                    options=['MySQL', 'MongoDB', 'InfluxDB'],
                    value='MySQL',
                    #on_change=lambda e: show_inputs_based_on_db(e.value)
                ).classes('rounded-md border border-[#2C25B2] px-4 py-2 text-md')
            with ui.row().classes('items-center gap-4'):
                ui.button(
                    'Advanced Database Configuration',
                    on_click=lambda: ui.navigate.to('/advanced-config'),
                ).classes('bg-orange-400 text-white mt-4 px-3 py-2 rounded-md text-sm')
            placeholder_column_inputs(main)

    ui.button('next', on_click=WriteFromFile.navigateFile).classes('mt-4')

def placeholder_column_inputs(container):
    """Draw initial 4 placeholder inputs inside a container"""
    with container:
        ui.input(placeholder='Height Column Name Here...').classes('border rounded-md border-[#3545FF]')
        ui.input(placeholder='Weight Column Name Here...').classes('border rounded-md border-[#3545FF]')
        ui.input(placeholder='Age Column Name Here...').classes('border rounded-md border-[#3545FF]')
        ui.input(placeholder='Gender Column Name Here...').classes('border rounded-md border-[#3545FF]')

# def show_inputs_based_on_db(db_type):
#     """Update inputs dynamically based on selected DB"""
#     ui.clean()
#     config()
