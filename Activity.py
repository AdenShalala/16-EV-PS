from nicegui import ui
import elements

def header():
    elements.header()

@ui.page('/activity')
def activity():
    header()
    with ui.row().classes('w-full'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
    with ui.grid(rows=10, columns=5).classes('w-full h-800px'):
        with ui.card().classes('col-span-1 row-span-10 border border-[#2C25B2]') as patients:
            ui.label("User Records")
        # with ui.column().classes('w-full row-span'):
        with ui.card().classes('col-span-4 row-span-7 border border-[#2C25B2]') as main:
            ui.label('plot here')
        with ui.row().classes('col-span-4 row-span-3'):
            with ui.grid(columns=3).classes('w-full h-full'):
                with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                    ui.label('Activity Recorded')
                with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                    ui.label('Area/s Exceeding Tolerance Level')
                with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                    ui.label('Type of Sensor/s Connected')
    # with ui.row().classes('w-full h-[800px]'):
        # with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
        #     ui.label("User Records")
        # with ui.column().classes('h-full w-full'):
        #     with ui.card().classes('w-3/4 h-2/3 border border-[#2C25B2]') as main:
        #         ui.label('plot here')
        #     with ui.row().classes('w-3/4 h-1/4'):
        #         with ui.card().classes('w-1/4 h-full border border-[#2C25B2]'):
        #             ui.label('Activity Recorded')
def navigateActivity():
    ui.navigate.to('/activity')

ui.run()