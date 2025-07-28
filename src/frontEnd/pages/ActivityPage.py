from nicegui import ui, app
import elements

def header():
    elements.header()

@ui.page('/activity')
def activityPage():
    ui.page_title("SocketFit Dashboard")
    header()
    # print(app.storage.user.get('activity'))
    print(app.storage.user.get('activity').type)
    # app.storage.user.get('activity').sensor
    # activity = app.storage.user.get('activity')
    with ui.row().classes('w-full'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[500px]'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.label("User Records")
        with ui.grid(rows=10).classes('w-3/4 h-800px'):
            with ui.card().classes('row-span-7 border border-[#2C25B2]') as main:
                ui.label('plot here')
            with ui.row().classes('row-span-3'):
                with ui.grid(columns=3).classes('w-full h-full'):
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Activity Recorded')
                        with ui.row():
                            ui.label(app.storage.user.get('activity').type)
                            ui.label(app.storage.user.get('activity').start_time)
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

# ui.run(storage_secret='this is the very secret key')