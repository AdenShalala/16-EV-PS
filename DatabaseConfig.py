from nicegui import ui
import elements
import WriteFromFile

def header():
    elements.header()

@ui.page('/config')
def config():
    ui.page_title("SocketFit Dashboard")
    header()
    with ui.row().classes('w-full'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.label("Database Configuration")
        with ui.card().classes('w-3/4 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            ui.input("Database Choice").classes('border rounded-md border-[#2C25B2]')
            ui.input(placeholder='Height Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Weight Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Age Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Gender Column Name Here...').classes('border rounded-md border-[#3545FF]')
    ui.button('next', on_click=WriteFromFile.navigateFile)

def navigateConfig():
    ui.navigate.to('/config')

ui.run()
ui.navigate.to('/config')