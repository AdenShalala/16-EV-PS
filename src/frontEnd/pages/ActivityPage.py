from nicegui import ui, app
import elements
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc

def header():
    elements.header()

@ui.page('/activity')
def activityPage():
    ui.page_title("SocketFit Dashboard")
    header()
    app.storage.user['dt_str1'] = app.storage.user.get('activity').start_time
    app.storage.user['dt_str2'] = app.storage.user.get('activity').end_time

    dt_format = "%d-%b-%Y %H:%M:%S"

    dt1 = datetime.strptime(app.storage.user.get('dt_str1'), dt_format)
    dt2 = datetime.strptime(app.storage.user.get('dt_str2'), dt_format)

    # app.storage.user['duration'] = dt2 - dt1
    total_seconds = int((dt2 - dt1).total_seconds())
    app.storage.user['total_seconds'] = total_seconds

    # app.storage.user['total_seconds'] = int(app.storage.user.get('duration').total_seconds())

    app.storage.user['hours'] = app.storage.user.get('total_seconds') // 3600
    app.storage.user['minutes'] = (app.storage.user.get('total_seconds') % 3600) // 60
    app.storage.user['seconds'] = app.storage.user['total_seconds'] % 60
    print(app.storage.user.get('activity').type)
    state = app.storage.user.get('state', {'playing': False, 'frame_index': 0})
    app.storage.user['state'] = state
    with ui.row().classes('w-full items-end'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
        ui.space()
        def toggle_play():
            state = app.storage.user.get('state')
            state['playing'] = not state['playing']
            if state['playing']:
                timer.activate()
                play_pause_icon.set_name('pause_circle')
            else:
                timer.deactivate()
                play_pause_icon.set_name('play_circle')

        with ui.button(color='#FFB030').classes('rounded-md text-white flex items-center gap-3 w-200px ml-[10%]').on_click(toggle_play) as btn:
            with ui.row().classes('w-full h-full text-align-middle'):
                with ui.column().classes('text-left'):
                    ui.label('Activity')
                    ui.label(f'{app.storage.user.get('hours'):02}:{app.storage.user.get('minutes'):02}:{app.storage.user.get('seconds'):02}')
                play_pause_icon = ui.icon('play_circle').classes('w-16 h-16 ml-4')

    with ui.row().classes('w-full h-[500px]'):
        with ui.card().classes('w-1/5 border border-[#2C25B2]') as patients:
            ui.label("User Records")
        with ui.grid(rows=10).classes('w-3/4 h-800px'):
            with ui.card().classes('row-span-7 border border-[#2C25B2]') as main:
                sensors = app.storage.user.get('activity').sensors
                timestamps = sensors[0].timestamp
                frame_count = len(timestamps)

                colors = pc.qualitative.Plotly
                fig = go.Figure()
                dot_trace_indices = []

                for i, sensor in enumerate(sensors):
                    color = colors[i % len(colors)]

                    fig.add_trace(go.Scatter(
                        x=sensor.timestamp,
                        y=sensor.signal,
                        name=sensor.location,
                        line=dict(color=color)
                    ))

                    fig.add_trace(go.Scatter(
                        x=[sensor.timestamp[0]],
                        y=[sensor.signal[0]],
                        mode='markers',
                        marker=dict(size=10, color=color),
                        name=f'{sensor.location} (dot)',
                        showlegend=False
                    ))

                    dot_trace_indices.append(len(fig.data) - 1)
                    fig.update_layout(hovermode='x unified', plot_bgcolor='white')
                    fig.update_xaxes(gridcolor='lightgrey')
                    fig.update_yaxes(gridcolor='lightgrey')

                plot = ui.plotly(fig).classes('w-full')
                plot._props['options']['config'] = {'displaylogo': False}

                app.storage.user['state'] = {
                    'frame_index': 0,
                    'playing': False
                }

                def update_dots():
                    if not app.storage.user.get('state')['playing']:
                        return

                    app.storage.user.get('state')['frame_index'] = (app.storage.user.get('state')['frame_index'] + 1) % frame_count

                    for i, sensor in enumerate(sensors):
                        dot_idx = dot_trace_indices[i]
                        fig.data[dot_idx].x = [sensor.timestamp[app.storage.user.get('state')['frame_index']]]
                        fig.data[dot_idx].y = [sensor.signal[app.storage.user.get('state')['frame_index']]]

                    plot.update()

                timer = ui.timer(interval=0.1, callback=update_dots, active=False)

            with ui.row().classes('row-span-3'):
                with ui.grid(columns=3).classes('w-full h-full'):
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Activity Recorded').classes('font-bold')
                        with ui.row():
                            ui.label(app.storage.user.get('activity').type)
                            ui.label(f'{app.storage.user.get('hours'):02}:{app.storage.user.get('minutes'):02}:{app.storage.user.get('seconds'):02}')
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Area/s Exceeding Tolerance Level').classes('font-bold')
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Type of Sensor/s Connected').classes('font-bold')
                        with ui.row():
                            app.storage.user['sensorTypeList'] = []
                            for app.storage.user['sensor'] in app.storage.user.get('activity').sensors:
                                if app.storage.user.get('sensor').type not in app.storage.user.get('sensorTypeList'):
                                    app.storage.user['sensorTypeList'].append(app.storage.user.get('sensor').type)
                            with ui.grid(columns=1):
                                for app.storage.user['item'] in app.storage.user.get('sensorTypeList'):
                                    ui.label(app.storage.user.get('item'))
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