from nicegui import ui, app
import pages.utilities as utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc
import api
colors = pc.qualitative.Plotly

def unix_to_datetime(unix_timestamp):
    """Convert Unix timestamp to datetime object."""
    if isinstance(unix_timestamp, str):
        unix_timestamp = float(unix_timestamp)
    return datetime.fromtimestamp(unix_timestamp)

def format_current_time(current_time):
    current_hours = int(current_time // 3600)
    current_minutes = int((current_time % 3600) // 60)
    current_seconds = int(current_time % 60)
    return f"{current_hours:02}:{current_minutes:02}:{current_seconds:02}"

def create() -> None:
    @ui.page("/activity")
    def activity():
        app.storage.user['current_page'] = '/activity'
        ui.page_title("SocketFit Dashboard")
        utilities.header()

        activity = api.get_activity(app.storage.user.get("selected_patient"), app.storage.user.get("selected_activity"), app.storage.user.get("token"))
        
        dt_str1 = utilities.normalize_to_str(activity.start_time)
        dt_str2 = utilities.normalize_to_str(activity.end_time)

        dt_format = "%d-%b-%Y %H:%M:%S"

        dt1 = datetime.strptime(dt_str1, dt_format)
        dt2 = datetime.strptime(dt_str2, dt_format)

        total_seconds = int((dt2 - dt1).total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        state = {'playing': False, 'current_time': 0, "current_time": 0}
        x_axis_unit = 'seconds'
        animation_speed = 1.0
        speed_value = {'current': 1.0}
        ui_elements = {}

        

        with ui.row().classes('w-full items-end'):
            ui.label("Activity").classes('text-xl font-semibold ml-[21%]')
            ui.space()
            
            # playing and pausing graph animation, setting play button to play or pause
            def toggle_play():
                state['playing'] = not state['playing']
                if state['playing']:
                    ui_elements['timer'].activate()
                    ui_elements['play_pause_icon'].set_name('pause_circle')
                else:
                    ui_elements['timer'].deactivate()
                    ui_elements['play_pause_icon'].set_name('play_circle')

            def toggle_x_axis_unit(e):
                new_unit = 'minutes' if x_axis_unit == 'seconds' else 'seconds'
                x_axis_unit = new_unit
            
                update_x_axis()    

            with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] mr-[4%] p-2 right').on_click(toggle_play):
                with ui.grid(columns=2).classes('w-full'):
                    with ui.column().classes('gap-0 items-start w-full'):
                        ui.label('Activity').classes('text-sm leading-tight m-0')
                        current_time_label = ui.label(format_current_time(state['current_time'])).classes('text-sm leading-tight m-0')
                    with ui.column().classes('items-end'):
                        play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;').props('justify-right')
            
            ui_elements['current_time_label'] = current_time_label
            ui_elements['play_pause_icon'] = play_pause_icon

        with ui.row().classes('w-full h-[500px]'):
            # left section for tree
            with ui.card().classes('w-1/5 border border-[#2C25B2]'):
                utilities.session_tree()
            with ui.grid(rows=10).classes('w-3/4 h-[800px]'):
                # main section for graph
                with ui.card().classes('row-span-7 border border-[#2C25B2]'):
                    with ui.row().classes('w-full justify-between items-center p-4 pb-2'):
                        with ui.row().classes('items-center gap-6 w-full'):
                            with ui.row().classes('items-center gap-2 w-full'):
                                ui.label('Speed:').classes('text-sm')
                                
                                def update_speed(e):
                                    new = float(e.args)
                                    speed_value["current"] = new
                                    animation_speed = new
                                    ui_elements['speed_label'].text = f"{new}x"
                                
                                ui.slider(min=0.1, max=100.0, step=0.1, value=1.0).props('label-always snap markers="[1, 5, 10, 25, 50, 100]"').classes('w-3/5').style('--q-primary: #FFB030').on('update:model-value', update_speed)
                                speed_label = ui.label("1.0x").classes('text-sm min-w-8')
                                ui_elements['speed_label'] = speed_label

                                with ui.row().classes('items-center gap-2'):
                                    ui.label('Seconds').classes('text-sm')
                                    x_axis_switch = ui.switch(value=False).on('update:model-value', toggle_x_axis_unit).style('--q-primary: #FFB030')
                                    ui.label('Minutes').classes('text-sm')

                    
                    fig = go.Figure()
                    dot_trace_indices = []
                    normalized_sensors = []

                    def get_display_values(timestamps_in_seconds, unit):
                        if unit == 'minutes':
                            return [t / 60 for t in timestamps_in_seconds]
                        return timestamps_in_seconds

                    def get_axis_label(unit):
                        return f"Time ({unit})"

                    def get_axis_range(unit):
                        if unit == 'minutes':
                            return [0, total_seconds / 60]
                        return [0, total_seconds]

                    # Get activity start time as datetime for calculations
                    activity_start_dt = unix_to_datetime(activity.start_time)

                    activity_readings = api.get_activity_readings(app.storage.user.get("selected_patient"), activity.activity_id, app.storage.user.get("token"))

                    for i, activity_reading in enumerate(activity_readings):
                        sensor = api.get_sensor(app.storage.user.get("selected_patient"), activity_reading.sensor_id, app.storage.user.get("token"))
                        
                        # sensor name with location and type for display on graph
                        sensor_name = f"{sensor.location_name.capitalize()} ({sensor.sensor_type})"
                        color = colors[i % len(colors)]
                        
                        # calculate timestamps and pressures for all readings in this sensor
                        timestamps_seconds = []
                        pressures = []
                        
                        pressure_readings = api.get_pressure_readings(app.storage.user.get("selected_patient"), activity.activity_id, activity_reading.reading_series_id, app.storage.user.get("token"))

                        for pressure_reading in pressure_readings:
                            reading_time = unix_to_datetime(pressure_reading.time)
                            
                            # calculate seconds elapsed from activity start
                            time_from_start_seconds = (reading_time - activity_start_dt).total_seconds()
                            
                            # clamp to activity bounds
                            time_from_start_seconds = max(0, min(time_from_start_seconds, total_seconds))
                            
                            timestamps_seconds.append(time_from_start_seconds)
                            pressures.append(float(pressure_reading.pressure_value))

                        # sort by timestamp
                        combined = list(zip(timestamps_seconds, pressures))
                        combined.sort(key=lambda x: x[0])
                        timestamps_seconds, pressures = zip(*combined) if combined else ([], [])
                        
                        # convert to lists
                        timestamps_seconds = list(timestamps_seconds)
                        pressures = list(pressures)

                        # store sensor data for animation and axis switching
                        normalized_sensors.append({
                            'timestamps': timestamps_seconds,
                            'signals': pressures,
                            'name': sensor_name
                        })

                        # get display values based on current unit
                        current_unit = x_axis_unit
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
                            dot_trace_indices.append(len(fig.data) - 1)

                    # update graph layout
                    current_unit = x_axis_unit
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
                        current_unit = x_axis_unit

                        for i, sensor_data in enumerate(normalized_sensors):
                            line_idx = i * 2  # line traces are at even indices
                            display_timestamps = get_display_values(sensor_data['timestamps'], current_unit)
                            fig.data[line_idx].x = display_timestamps
                        
                        current_time = state["current_time"]
                        display_current_time = current_time / 60 if current_unit == 'minutes' else current_time
                        
                        for i, sensor_data in enumerate(normalized_sensors):
                            if i < len(dot_trace_indices):
                                dot_idx = dot_trace_indices[i]
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
                        if not state or not state.get('playing'):
                            return

                        current_speed = speed_value["current"]
                        time_increment = base_time_increment * current_speed

                        current_time = state['current_time']
                        current_time += time_increment
                        
                        if current_time >= total_seconds:
                            current_time = 0
                        
                        state['current_time'] = current_time

                        ui_elements['current_time_label'].text = format_current_time(current_time)

                        current_unit = x_axis_unit
                        display_current_time = current_time / 60 if current_unit == 'minutes' else current_time

                        for i, sensor_data in enumerate(normalized_sensors):
                            if i < len(dot_trace_indices):
                                dot_idx = dot_trace_indices[i]
                                
                                signal_value = interpolate_signal(
                                    sensor_data["timestamps"],
                                    sensor_data['signals'], 
                                    current_time
                                )
                                
                                fig.data[dot_idx].x = [display_current_time]
                                fig.data[dot_idx].y = [signal_value]

                        ui_elements['plot'].update()

                    timer = ui.timer(interval=0.1, callback=update_dots, active=False)
                    ui_elements['timer'] = timer
                
                toleranceList = []

                with ui.row().classes('row-span-3'):
                    with ui.grid(columns=3).classes('w-full h-full'):
                        # information about activity
                        with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                            ui.label('Activity Recorded').classes('font-bold')
                            with ui.row():
                                ui.label(activity.activity_type)
                                ui.label(f'{hours:02}:{minutes:02}:{seconds:02}')
                        # list of areas exceeding tolerance levels
                        with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                            ui.label('Area/s Exceeding Tolerance Level').classes('font-bold')
                        # list of sensor types
                        with ui.card().classes('col-span-1 h-full border border-[#2C25B2]'):
                            ui.label('Type of Sensor/s Connected').classes('font-bold')
                            with ui.row():
                                sensorTypeList= []
                                for i, activity_reading in enumerate(activity_readings):
                                    sensor = api.get_sensor(app.storage.user.get("selected_patient"), activity_reading.sensor_id, app.storage.user.get("token"))
                                    if sensor.sensor_type not in sensorTypeList:
                                        sensorTypeList.append(sensor.sensor_type)
                                with ui.grid(columns=1):
                                    for item in sensorTypeList:
                                        ui.label(item)
