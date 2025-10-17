from nicegui import ui, app
import pages.utilities as utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc
import api
colors = pc.qualitative.Plotly

def unix_to_datetime(unix_timestamp):
    if isinstance(unix_timestamp, str):
        unix_timestamp = float(unix_timestamp)
    return datetime.fromtimestamp(unix_timestamp)

def format_current_time(current_time):
    current_hours = int(current_time // 3600)
    current_minutes = int((current_time % 3600) // 60)
    current_seconds = int(current_time % 60)
    return f"{current_hours:02}:{current_minutes:02}:{current_seconds:02}"

showActivity = []
activityGraphsContainer = None

def create_activity_graph(activity, activity_index):
    
    dt_str1 = utilities.normalize_to_str(activity.start_time)
    dt_str2 = utilities.normalize_to_str(activity.end_time)
    dt_format = "%d-%b-%Y %H:%M:%S"
    dt1 = datetime.strptime(dt_str1, dt_format)
    dt2 = datetime.strptime(dt_str2, dt_format)
    total_seconds = int((dt2 - dt1).total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    state = {'playing': False, 'current_time': 0}
    x_axis_unit = {'current': 'seconds'}
    speed_value = {'current': 1.0}
    ui_elements = {}

    def toggle_play():
        state['playing'] = not state['playing']
        if state['playing']:
            ui_elements['timer'].activate()
            ui_elements['play_pause_icon'].set_name('pause_circle')
        else:
            ui_elements['timer'].deactivate()
            ui_elements['play_pause_icon'].set_name('play_circle')

    def toggle_x_axis_unit(e):
        if x_axis_unit['current'] == 'seconds':
            x_axis_unit['current'] = 'minutes'
        else:
            x_axis_unit['current'] = 'seconds'
        update_x_axis()

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

    with ui.card().classes('w-full border border-[#2C25B2] mb-4'):
        with ui.row().classes('w-full items-center justify-between p-4 pb-2'):
            ui.label(f'{activity.activity_type} - {dt_str1}').classes('text-lg font-semibold')
            
            with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] p-2').on_click(toggle_play):
                with ui.grid(columns=2).classes('w-full'):
                    with ui.column().classes('gap-0 items-start w-full'):
                        ui.label('Activity').classes('text-sm leading-tight m-0')
                        current_time_label = ui.label(format_current_time(state['current_time'])).classes('text-sm leading-tight m-0')
                    with ui.column().classes('items-end'):
                        play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;')
            
            ui_elements['current_time_label'] = current_time_label
            ui_elements['play_pause_icon'] = play_pause_icon

        with ui.row().classes('w-full justify-between items-center p-4 pb-2'):
            with ui.row().classes('items-center gap-6 w-full'):
                with ui.row().classes('items-center gap-2 w-full'):
                    ui.label('Speed:').classes('text-sm')
                    
                    def update_speed(e):
                        new = float(e.args)
                        speed_value["current"] = new
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

        activity_start_dt = unix_to_datetime(activity.start_time)
        activity_readings = api.get_activity_readings(
            app.storage.user.get("selected_patient"), 
            activity.activity_id, 
            app.storage.user.get("token")
        )

        for i, activity_reading in enumerate(activity_readings):
            sensor = api.get_sensor(
                app.storage.user.get("selected_patient"), 
                activity_reading.sensor_id, 
                app.storage.user.get("token")
            )
            
            sensor_name = f"{sensor.location_name.capitalize()} ({sensor.sensor_type})"
            color = colors[i % len(colors)]
            
            timestamps_seconds = []
            pressures = []
            
            pressure_readings = api.get_pressure_readings(
                app.storage.user.get("selected_patient"), 
                activity.activity_id, 
                activity_reading.reading_series_id, 
                app.storage.user.get("token")
            )

            for pressure_reading in pressure_readings:
                reading_time = unix_to_datetime(pressure_reading.time)
                time_from_start_seconds = (reading_time - activity_start_dt).total_seconds()
                time_from_start_seconds = max(0, min(time_from_start_seconds, total_seconds))
                
                timestamps_seconds.append(time_from_start_seconds)
                pressures.append(float(pressure_reading.pressure_value))

            combined = list(zip(timestamps_seconds, pressures))
            combined.sort(key=lambda x: x[0])
            timestamps_seconds, pressures = zip(*combined) if combined else ([], [])
            
            timestamps_seconds = list(timestamps_seconds)
            pressures = list(pressures)

            normalized_sensors.append({
                'timestamps': timestamps_seconds,
                'signals': pressures,
                'name': sensor_name
            })

            current_unit = x_axis_unit['current']
            display_timestamps = get_display_values(timestamps_seconds, current_unit)

            fig.add_trace(go.Scatter(
                x=display_timestamps,
                y=pressures,
                name=sensor_name,
                line=dict(color=color)
            ))

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

        current_unit = x_axis_unit['current']
        fig.update_layout(
            hovermode='x unified', 
            plot_bgcolor='white',
            xaxis_title=get_axis_label(current_unit),
            yaxis_title="Pressure",
            height=400
        )
        fig.update_xaxes(gridcolor='lightgrey', range=get_axis_range(current_unit))
        fig.update_yaxes(gridcolor='lightgrey')

        plot = ui.plotly(fig).classes('w-full')
        plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}
        ui_elements['plot'] = plot      

        def update_x_axis():
            current_unit = x_axis_unit['current']

            for i, sensor_data in enumerate(normalized_sensors):
                line_idx = i * 2
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

            current_unit = x_axis_unit['current']
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

def update_activity_graphs():
    global activityGraphsContainer
    if activityGraphsContainer is not None:
        activityGraphsContainer.clear()
    if activityGraphsContainer is not None and showActivity:
        with activityGraphsContainer:
            for idx, activity in enumerate(showActivity):
                create_activity_graph(activity, idx)

def create() -> None:
    global activityGraphsContainer
    
    @ui.page("/activity")
    def activity():
        global activityGraphsContainer
        
        app.storage.user['current_page'] = '/activity'
        if app.storage.user.get('darkbool') == True:
            dark = ui.dark_mode()
            dark.enable()
        ui.page_title("SocketFit Dashboard")
        utilities.header()
        utilities.sidebar() 
        
        with ui.row().classes('w-full'):
            patient = api.get_patient(
                patient_id=app.storage.user.get("selected_patient"), 
                token=app.storage.user.get('token')
            )
            patient_name = f"{patient.first_name} {patient.last_name}'s Activities"
            ui.label(patient_name).classes('text-xl font-semibold')
        
        activity_container = ui.column().classes('w-full')
        activities = api.get_activities(
            patient_id=app.storage.user.get("selected_patient"), 
            token=app.storage.user.get("token")
        )
        
        with activity_container:
            with ui.row().classes('w-full'):
                with ui.card().classes('w-9/10 border rounded-md border-[#3545FF]'):
                    with ui.card().classes('w-full shadow-0 p-0 items-start'):        

                        with ui.grid(columns=24).classes('w-full font-bold'):
                            ui.label('').classes('col-span-1')
                            ui.label('Date').classes('col-span-3')
                            ui.label('').classes('col-span-3')
                            ui.label('Activity').classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label('Duration').classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label('Pressure').classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label('').classes('col-span-1')
                    
                    for activity in activities:
                        dt_str1 = utilities.normalize_to_str(activity.start_time)
                        dt_str2 = utilities.normalize_to_str(activity.end_time)
                        dt_format = "%d-%b-%Y %H:%M:%S"
                        dt1 = datetime.strptime(dt_str1, dt_format)
                        dt2 = datetime.strptime(dt_str2, dt_format)
                        total_seconds = int((dt2 - dt1).total_seconds())
                        
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60
                        
                        minSensor, maxSensor = None, None
                        readings = api.get_activity_readings(
                            app.storage.user.get("selected_patient"), 
                            activity.activity_id, 
                            app.storage.user.get("token")
                        )
                        
                        for reading in readings:
                            pressure = api.get_pressure_readings(
                                app.storage.user.get("selected_patient"), 
                                activity.activity_id, 
                                reading.reading_series_id, 
                                app.storage.user.get("token")
                            )
                            
                            for x in pressure:
                                value = float(x.pressure_value)
                                if minSensor is None or value < minSensor:
                                    minSensor = round(value, 1)
                                if maxSensor is None or value > maxSensor:
                                    maxSensor = round(value, 1)
                        
                        def make_change_handler(act):
                            def handler(e):
                                if e.value:
                                    if act not in showActivity:
                                        showActivity.append(act)
                                else:
                                    if act in showActivity:
                                        showActivity.remove(act)
                                update_activity_graphs()
                            return handler
                        
                        
                       
                        with ui.grid(columns=24).classes('border-[2px] border-[#2C25B2] h-16 rounded items-center'):
                            ui.label('').classes('col-span-1')
                            ui.label(utilities.normalize_to_str(activity.start_time)).classes('col-span-3')
                            ui.label('').classes('col-span-3')
                            ui.label(activity.activity_type).classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label(f'{hours}h{minutes}m{seconds}s').classes('col-span-2')
                            ui.label('').classes('col-span-3')
                            ui.label(f"{minSensor} - {maxSensor}").classes('col-span-2')
                            ui.label('').classes('col-span-2')
                            ui.checkbox('Display Activity', value=False, on_change=make_change_handler(activity)).style('--q-primary: #FFB030').classes('col-span-2')
                            ui.label('').classes('col-span-1')             
                    ui.space()
            
            activityGraphsContainer = ui.column().classes('w-full mt-4')