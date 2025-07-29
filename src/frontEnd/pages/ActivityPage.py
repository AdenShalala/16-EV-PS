from nicegui import ui, app
import elements
import plotly.graph_objects as go

def header():
    elements.header()

@ui.page('/activity')
def activityPage():
    ui.page_title("SocketFit Dashboard")
    header()
    print(app.storage.user.get('activity').type)
    with ui.row().classes('w-full'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
    with ui.row().classes('w-full h-[500px]'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.label("User Records")
        with ui.grid(rows=10).classes('w-3/4 h-800px'):
            with ui.card().classes('row-span-7 border border-[#2C25B2]') as main:
                fig = go.Figure()
                for sensor in app.storage.user.get('activity').sensors:
                    fig.add_trace(go.Scatter(x=sensor.timestamp, y=sensor.signal, name=sensor.location))
                fig.update_layout(hovermode='x unified', plot_bgcolor='white')
                fig.update_xaxes(gridcolor='lightgrey')
                fig.update_yaxes(gridcolor='lightgrey')
                
                with ui.row().classes('w-full h-full'):
                    ui.plotly(fig).classes('w-full')
            with ui.row().classes('row-span-3'):
                with ui.grid(columns=3).classes('w-full h-full'):
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Activity Recorded').classes('font-bold')
                        with ui.row():
                            ui.label(app.storage.user.get('activity').type)
                            ui.label(app.storage.user.get('activity').start_time)
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Area/s Exceeding Tolerance Level').classes('font-bold')
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Type of Sensor/s Connected').classes('font-bold')
                        with ui.row():
                            sensorTypeList = []
                            for sensor in app.storage.user.get('activity').sensors:
                                if sensor.type not in sensorTypeList:
                                    sensorTypeList.append(sensor.type)
                            with ui.grid(columns=1):
                                for item in sensorTypeList:
                                    ui.label(item)
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