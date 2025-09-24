from nicegui import ui, app
import utilities
import SessionHistory
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc

# getting standard header
def header():
    utilities.header()

def unix_to_datetime(unix_timestamp):
    """Convert Unix timestamp to datetime object."""
    if isinstance(unix_timestamp, str):
        unix_timestamp = float(unix_timestamp)
    return datetime.fromtimestamp(unix_timestamp)

@ui.page('/activity')
def activityPage():
    app.storage.user['current_page'] = '/activity'
    ui.page_title("SocketFit Dashboard")
    header()
    # calculating duration
    app.storage.user['dt_str1'] = SessionHistory.normalize_to_str(app.storage.user.get('activity').start_time)
    app.storage.user['dt_str2'] = SessionHistory.normalize_to_str(app.storage.user.get('activity').end_time)

    dt_format = "%d-%b-%Y %H:%M:%S"

    dt1 = datetime.strptime(app.storage.user.get('dt_str1'), dt_format)
    dt2 = datetime.strptime(app.storage.user.get('dt_str2'), dt_format)

    app.storage.user['total_seconds'] = int((dt2 - dt1).total_seconds())

    app.storage.user['hours'] = app.storage.user.get('total_seconds') // 3600
    app.storage.user['minutes'] = (app.storage.user.get('total_seconds') % 3600) // 60
    app.storage.user['seconds'] = app.storage.user['total_seconds'] % 60
    
    app.storage.user['state'] = {'playing': False, 'current_time': 0}
    app.storage.user['x_axis_unit'] = 'seconds'
    app.storage.user['animation_speed'] = 1.0
    app.storage.user['speed_value'] = {'current': 1.0}
    

    ui_elements = {}
    app.storage.user['state']['current_time'] = 0
    
    def format_current_time(current_time):
        app.storage.user['current_hours'] = int(current_time // 3600)
        app.storage.user['current_minutes'] = int((current_time % 3600) // 60)
        app.storage.user['current_seconds'] = int(current_time % 60)
        return f"{app.storage.user.get('current_hours'):02}:{app.storage.user.get('current_minutes'):02}:{app.storage.user.get('current_seconds'):02}"
    
    with ui.row().classes('w-full items-end'):
        ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
        ui.space()
        
        # playing and pausing graph animation, setting play button to play or pause
        def toggle_play():
            app.storage.user.get('state')['playing'] = not app.storage.user.get('state')['playing']
            if app.storage.user.get('state')['playing']:
                ui_elements['timer'].activate()
                ui_elements['play_pause_icon'].set_name('pause_circle')
            else:
                ui_elements['timer'].deactivate()
                ui_elements['play_pause_icon'].set_name('play_circle')
        
        # button to play and pause animation
        with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] mr-[4%] p-2 right').on_click(toggle_play):
            with ui.grid(columns=2).classes('w-full'):
                with ui.column().classes('gap-0 items-start w-full'):
                    ui.label('Activity').classes('text-sm leading-tight m-0')
                    current_time_label = ui.label(format_current_time(app.storage.user.get('state')['current_time'])).classes('text-sm leading-tight m-0')
                with ui.column().classes('items-end'):
                    play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;').props('justify-right')
        
        ui_elements['current_time_label'] = current_time_label
        ui_elements['play_pause_icon'] = play_pause_icon

    def toggle_x_axis_unit(e):
        app.storage.user['new_unit'] = 'minutes' if app.storage.user.get('x_axis_unit') == 'seconds' else 'seconds'
        app.storage.user['x_axis_unit'] = app.storage.user.get('new_unit')
        
        update_x_axis()

    with ui.row().classes('w-full h-[500px]'):
        # left section for tree
        with ui.card().classes('w-1/5 border border-[#2C25B2]'):
            utilities.session_tree()
        with ui.grid(rows=10).classes('w-3/4 h-800px'):
            # main section for graph
            with ui.card().classes('row-span-7 border border-[#2C25B2]'):
                with ui.row().classes('w-full justify-between items-center p-4 pb-2'):
                    with ui.row().classes('items-center gap-6 w-full'):
                        with ui.row().classes('items-center gap-2 w-full'):
                            ui.label('Speed:').classes('text-sm')
                            
                            app.storage.user['speed_value'] = app.storage.user.get('speed_value', {'current': 1.0})
                            
                            def update_speed(e):
                                app.storage.user['new_value'] = float(e.args)
                                app.storage.user.get('speed_value')['current'] = app.storage.user.get('new_value')
                                app.storage.user['animation_speed'] = app.storage.user.get('new_value')
                                ui_elements['speed_label'].text = f"{app.storage.user.get('new_value')}x"
                            
                            speed_slider = ui.slider(min=0.1, max=100.0, step=0.1, value=1.0).props('label-always snap markers="[1, 5, 10, 25, 50, 100]"').classes('w-3/5').style('--q-primary: #FFB030').on('update:model-value', update_speed)
                            speed_label = ui.label("1.0x").classes('text-sm min-w-8')
                            ui_elements['speed_label'] = speed_label

                            with ui.row().classes('items-center gap-2'):
                                ui.label('Seconds').classes('text-sm')
                                x_axis_switch = ui.switch(value=False).on('update:model-value', toggle_x_axis_unit).style('--q-primary: #FFB030')
                                ui.label('Minutes').classes('text-sm')

                colors = pc.qualitative.Plotly
                fig = go.Figure()
                app.storage.user['dot_trace_indices'] = []
                app.storage.user['normalized_sensors'] = []

                def get_display_values(timestamps_in_seconds, unit):
                    if unit == 'minutes':
                        return [t / 60 for t in timestamps_in_seconds]
                    return timestamps_in_seconds

                def get_axis_label(unit):
                    return f"Time ({unit})"

                def get_axis_range(unit):
                    if unit == 'minutes':
                        return [0, app.storage.user.get('total_seconds') / 60]
                    return [0, app.storage.user.get('total_seconds')]

                # Get activity start time as datetime for calculations
                activity_start_dt = unix_to_datetime(app.storage.user.get('activity').start_time)

                for app.storage.user['i'], app.storage.user['sensor'] in enumerate(app.storage.user.get('activity').sensors):
                    sensor_name = f"{app.storage.user.get('sensor').location} ({app.storage.user.get('sensor').type})"
                    color = colors[app.storage.user.get('i') % len(colors)]
                    
                    # calculate timestamps and pressures for all readings in this sensor
                    timestamps_seconds = []
                    pressures = []
                    
                    for reading in app.storage.user.get('sensor').readings:
                        if reading.activity_id == app.storage.user.get('activity').activity_id:
                            reading_time = unix_to_datetime(reading.time)
                            
                            # calculate seconds elapsed from activity start
                            time_from_start_seconds = (reading_time - activity_start_dt).total_seconds()
                            
                            # clamp to activity bounds
                            time_from_start_seconds = max(0, min(time_from_start_seconds, app.storage.user.get('total_seconds')))
                            
                            timestamps_seconds.append(time_from_start_seconds)
                            pressures.append(float(reading.pressure_value))

                    # sort by timestamp
                    combined = list(zip(timestamps_seconds, pressures))
                    combined.sort(key=lambda x: x[0])  # Sort by timestamp
                    timestamps_seconds, pressures = zip(*combined) if combined else ([], [])
                    
                    # convert to lists
                    timestamps_seconds = list(timestamps_seconds)
                    pressures = list(pressures)

                    # store sensor data for animation and axis switching
                    app.storage.user.get('normalized_sensors').append({
                        'timestamps': timestamps_seconds,
                        'signals': pressures,
                        'name': sensor_name
                    })

                    # get display values based on current unit
                    current_unit = app.storage.user.get('x_axis_unit')
                    display_timestamps = get_display_values(timestamps_seconds, current_unit)

                    # add line trace
                    fig.add_trace(go.Scatter(
                        x=display_timestamps,
                        y=pressures,
                        name=sensor_name,
                        line=dict(color=color)
                    ))

                    # add marker trace
                    if display_timestamps and pressures:
                        fig.add_trace(go.Scatter(
                            x=[display_timestamps[0]],
                            y=[pressures[0]],
                            mode='markers',
                            marker=dict(size=10, color=color),
                            name=sensor_name,
                            showlegend=False
                        ))
                        app.storage.user.get('dot_trace_indices').append(len(fig.data) - 1)

                # update graph layout
                current_unit = app.storage.user.get('x_axis_unit')
                fig.update_layout(
                    hovermode='x unified', 
                    plot_bgcolor='white',
                    xaxis_title=get_axis_label(current_unit),
                    yaxis_title="Pressure"
                )
                fig.update_xaxes(gridcolor='lightgrey', range=get_axis_range(current_unit))
                fig.update_yaxes(gridcolor='lightgrey')

                plot = ui.plotly(fig).classes('w-full')
                ui_elements['plot'] = plot
                
                # hiding some buttons from graph
                plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}

                def update_x_axis():
                    current_unit = app.storage.user.get('x_axis_unit')
                    for i, sensor_data in enumerate(app.storage.user.get('normalized_sensors')):
                        line_idx = i * 2  # line traces are at even indices
                        display_timestamps = get_display_values(sensor_data['timestamps'], current_unit)
                        fig.data[line_idx].x = display_timestamps
                    
                    current_time = app.storage.user.get('state')['current_time']
                    display_current_time = current_time / 60 if current_unit == 'minutes' else current_time
                    
                    for i, sensor_data in enumerate(app.storage.user.get('normalized_sensors')):
                        if i < len(app.storage.user.get('dot_trace_indices')):
                            dot_idx = app.storage.user.get('dot_trace_indices')[i]
                            fig.data[dot_idx].x = [display_current_time]
                    
                    fig.update_layout(xaxis_title=get_axis_label(current_unit))
                    fig.update_xaxes(range=get_axis_range(current_unit))
                    
                    ui_elements['plot'].update()

                updates_per_second = 10
                base_time_increment = 1.0 / updates_per_second  

                def interpolate_signal(timestamps, signals, target_time):
                    if not timestamps or not signals:
                        return 0
                    if target_time <= timestamps[0]:
                        return signals[0]
                    if target_time >= timestamps[-1]:
                        return signals[-1]
                    
                    for i in range(len(timestamps) - 1):
                        if timestamps[i] <= target_time <= timestamps[i + 1]:
                            t1, t2 = timestamps[i], timestamps[i + 1]
                            s1, s2 = signals[i], signals[i + 1]
                            ratio = (target_time - t1) / (t2 - t1) if t2 != t1 else 0
                            return s1 + ratio * (s2 - s1)
                    
                    return signals[-1] if signals else 0

                # moving markers based on time
                def update_dots():
                    state = app.storage.user.get('state')
                    if not state or not state.get('playing'):
                        return

                    app.storage.user['current_speed'] = app.storage.user.get('speed_value', {'current': 1.0})['current']
                    app.storage.user['time_increment'] = base_time_increment * app.storage.user.get('current_speed')

                    current_time = state['current_time']
                    current_time += app.storage.user.get('time_increment')
                    
                    if current_time >= app.storage.user.get('total_seconds'):
                        current_time = 0
                    
                    state['current_time'] = current_time

                    ui_elements['current_time_label'].text = format_current_time(current_time)

                    current_unit = app.storage.user.get('x_axis_unit')
                    display_current_time = current_time / 60 if current_unit == 'minutes' else current_time

                    for app.storage.user['i'], app.storage.user['sensor_data'] in enumerate(app.storage.user.get('normalized_sensors')):
                        if app.storage.user.get('i') < len(app.storage.user.get('dot_trace_indices')):
                            dot_idx = app.storage.user.get('dot_trace_indices')[app.storage.user.get('i')]
                            
                            signal_value = interpolate_signal(
                                app.storage.user.get('sensor_data')['timestamps'], 
                                app.storage.user.get('sensor_data')['signals'], 
                                current_time
                            )
                            
                            fig.data[dot_idx].x = [display_current_time]
                            fig.data[dot_idx].y = [signal_value]

                    ui_elements['plot'].update()

                timer = ui.timer(interval=0.1, callback=update_dots, active=False)
                ui_elements['timer'] = timer
            
            app.storage.user['toleranceList'] = []

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