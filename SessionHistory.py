from nicegui import ui
import elements

def header():
    elements.header()

@ui.page('/sessionHistory')
def sessionHistory():
    header()
    activityList = ['All']
    with ui.row().classes('w-full'):
        ui.label("User History").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[800px]'):
        with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            ui.label("User Records")
        with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
            ui.label("Filters:")
            with ui.grid(columns=11).classes('w-full'):
                # ui.label('').classes('col-span-1')
                ui.label("Activity").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Duration").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label("Pressure Range").classes('col-span-2')
                ui.label('').classes('col-span-1')
                ui.label('Pressure Tolerance').classes('col-span-2')
                # ui.label('').classes('col-span-1')
            with ui.grid(columns=11).classes('w-full'):
                # ui.label('').classes('col-span-1')
                ui.select(options=activityList, value=activityList[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.label('').classes('col-span-1')
                ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
            ui.label("Session List").classes('text-2xl')
            with ui.row().classes('w-full'):
                ui.space()
                with ui.card().classes('w-9/10 border rounded-md border-[#3545FF]'):
                    with ui.grid(columns=23):
                        ui.label('').classes('col-span-1')
                        ui.label('Session ID').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Date').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Activity').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Duration').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('Pressure').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                        ui.label('').classes('col-span-2')
                ui.space()


def navigateSession():
    ui.navigate.to('sessionHistory')