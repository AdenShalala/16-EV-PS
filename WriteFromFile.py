from nicegui import ui
import elements

def header():
    elements.header()

@ui.page('/writeFile')
def writeFile():
    header()
    with ui.grid(rows=10, columns=5).classes('w-full h-800px'):
        with ui.card().classes('col-span-1 row-span-10 border border-[#2C25B2]') as patients:
            ui.label("Write to Database from File")
        with ui.card().classes('col-span-4 row-span-10 border rounded-md border-[#2C25B2] justify-center items-center') as main:
            ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full')
            ui.input("Database Choice").classes('border rounded-md border-[#2C25B2]')
            ui.input(placeholder='Height Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Weight Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Age Column Name Here...').classes('border rounded-md border-[#3545FF]')
            ui.input(placeholder='Gender Column Name Here...').classes('border rounded-md border-[#3545FF]')

def navigateFile():
    ui.navigate.to('/writeFile')

ui.run()
ui.navigate.to('/writeFile')