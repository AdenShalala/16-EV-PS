from nicegui import ui, app
import utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc

# getting standard header
def header():
    utilities.header()

@ui.page('/activity')
def activityPage():
    ui.page_title("SocketFit Dashboard")
    header()
    # calculating duration
    app.storage.user['dt_str1'] = app.storage.user.get('activity').start_time
    app.storage.user['dt_str2'] = app.storage.user.get('activity').end_time

    dt_format = "%d-%b-%Y %H:%M:%S"

    dt1 = datetime.strptime(app.storage.user.get('dt_str1'), dt_format)
    dt2 = datetime.strptime(app.storage.user.get('dt_str2'), dt_format)

    app.storage.user['total_seconds'] = int((dt2 - dt1).total_seconds())

    app.storage.user['hours'] = app.storage.user.get('total_seconds') // 3600
    app.storage.user['minutes'] = (app.storage.user.get('total_seconds') % 3600) // 60
    app.storage.user['seconds'] = app.storage.user['total_seconds'] % 60
    # getting playing state of graph
    state = app.storage.user.get('state', {'playing': False, 'frame_index': 0})
    app.storage.user['state'] = state
    with ui.row().classes('w-full items-end'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
        ui.space()
        # playing and pausing graph animation, setting play button to play or pause
        def toggle_play():
            state = app.storage.user.get('state')
            state['playing'] = not state['playing']
            if state['playing']:
                timer.activate()
                play_pause_icon.set_name('pause_circle')
            else:
                timer.deactivate()
                play_pause_icon.set_name('play_circle')
        
        # button to play and pause animation
        with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] mr-[4%] p-2 right').on_click(toggle_play):
            with ui.grid(columns=2).classes('w-full'):
                with ui.column().classes('gap-0 items-start w-full'):
                    ui.label('Activity').classes('text-sm leading-tight m-0')
                    ui.label(f"{app.storage.user.get('hours'):02}:{app.storage.user.get('minutes'):02}:{app.storage.user.get('seconds'):02}") \
                        .classes('text-sm leading-tight m-0')
                with ui.column().classes('items-end'):
                    play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;').props('justify-right')

    with ui.row().classes('w-full h-[500px]'):
        # left section for tree
        with ui.card().classes('w-1/5 border border-[#2C25B2]'):
            utilities.session_tree()
        with ui.grid(rows=10).classes('w-3/4 h-800px'):
            # main section for graph
            with ui.card().classes('row-span-7 border border-[#2C25B2]'):
                sensors = app.storage.user.get('activity').sensors
                timestamps = sensors[0].timestamp
                frame_count = len(timestamps)

                # plotly graph
                colors = pc.qualitative.Plotly
                fig = go.Figure()
                dot_trace_indices = []

                for i, sensor in enumerate(sensors):
                    app.storage.user['name'] = f"{sensor.location} ({sensor.type})"
                    color = colors[i % len(colors)]

                    # adding traces for line
                    fig.add_trace(go.Scatter(
                        x=sensor.timestamp,
                        y=sensor.signal,
                        name=app.storage.user.get('name'),
                        line=dict(color=color)
                    ))

                    # adding traces for markers
                    fig.add_trace(go.Scatter(
                        x=[sensor.timestamp[0]],
                        y=[sensor.signal[0]],
                        mode='markers',
                        marker=dict(size=10, color=color),
                        name=app.storage.user.get('name'),
                        showlegend=False
                    ))

                    dot_trace_indices.append(len(fig.data) - 1)
                    # changing graph look
                    fig.update_layout(hovermode='x unified', plot_bgcolor='white')
                    fig.update_xaxes(gridcolor='lightgrey')
                    fig.update_yaxes(gridcolor='lightgrey')

                plot = ui.plotly(fig).classes('w-full')
                # hiding some buttons from graph
                plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}

                app.storage.user['state'] = {
                    'frame_index': 0,
                    'playing': False
                }

                # moving markers
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
            
            toleranceList = []
            # getting tolerances
            for app.storage.user['sensor'] in app.storage.user.get('activity').sensors:
                for app.storage.user['signal'] in app.storage.user.get('sensor').signal:
                    if float(app.storage.user.get('signal')) > float(app.storage.user.get('sensor').pressure_tolerance):
                        toleranceList.append(app.storage.user.get('signal'))

            with ui.row().classes('row-span-3'):
                with ui.grid(columns=3).classes('w-full h-full'):
                    # information about activity
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Activity Recorded').classes('font-bold')
                        with ui.row():
                            ui.label(app.storage.user.get('activity').type)
                            ui.label(f'{app.storage.user.get('hours'):02}:{app.storage.user.get('minutes'):02}:{app.storage.user.get('seconds'):02}')
                    # list of areas exceeding tolerance levels
                    with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                        ui.label('Area/s Exceeding Tolerance Level').classes('font-bold')
                        with ui.scroll_area().classes('h-20'):
                            for tolerance in toleranceList:
                                ui.label(tolerance)
                    # list of sensor types
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

def navigateActivity():
    ui.navigate.to('/activity')