from nicegui import ui
import elements
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'backEnd', 'databases', 'SQL')))
from fileXMLintoSQL import create_database

import asyncio

def header():
    elements.header()

@ui.page('/writeFile')
def writeFile():
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.link('Database Configuration', '/config').style('color: black; text-decoration: none;')
            ui.link('Write From File', '/writeFile').style('color: black; text-decoration: none;')
        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            
            async def handle_database_upload(e):
                try:
                    xml_content = e.content.read().decode('utf-8')
                    ui.notify("File uploaded, processing in background...")

                    await asyncio.to_thread(create_database, xml_content)
                    ui.notify("Data inserted successfully!")

                except Exception as err:
                    ui.notify(f"Failed to handle file: {str(err)}")

            ui.upload(
                label='Drag and drop or browse for XML file',
                on_upload=handle_database_upload,
                auto_upload=True,
                max_files=1,
            ).props('accept=".xml"').style('color: #3545FF; text-transform: none;').classes('rounded-md px-4 py-2')
            ui.input("Database Choice").classes('border rounded-md border-[#2C25B2]')
            ui.input(placeholder='Height Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Weight Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Age Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Gender Column Name Here...').classes('border rounded-md border-[#3545FF]')
            
def navigateFile():
    ui.navigate.to('/writeFile')

# ui.run()
ui.navigate.to('/writeFile')