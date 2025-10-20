from nicegui import ui, app
import pages.utilities as utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc
import api
colors = pc.qualitative.Plotly

def get_display_values(timestamps_in_seconds, unit):
    if unit == 'minutes':
        return [t / 60 for t in timestamps_in_seconds]
    return timestamps_in_seconds

def setFigStyling(fig):
    fig.update_layout(
        hovermode='x unified',
        autosize=True,
        showlegend=True,
    )

    if app.storage.user.get('dark_mode') == True:
        fig.update_layout(
            plot_bgcolor='#0A0A0A',
            paper_bgcolor='#0A0A0A',
            font_color='white',
        )
        fig.update_xaxes(linecolor='grey', gridcolor='grey', zeroline=True, zerolinecolor='white', zerolinewidth=1)
        fig.update_yaxes(linecolor='grey', gridcolor='grey', zeroline=True, zerolinecolor='white', zerolinewidth=1)
    else:
        fig.update_layout(
            plot_bgcolor='#F5F5F5',
            paper_bgcolor='#F5F5F5',
            font_color='black',
        )
        fig.update_xaxes(linecolor='black', gridcolor='lightgrey', zeroline=True, zerolinecolor='black', zerolinewidth=1)
        fig.update_yaxes(linecolor='black', gridcolor='lightgrey', zeroline=True, zerolinecolor='black', zerolinewidth=1)


def format_current_time(current_time):
    current_hours = int(current_time // 3600)
    current_minutes = int((current_time % 3600) // 60)
    current_seconds = int(current_time % 60)
    return f"{current_hours:02}:{current_minutes:02}:{current_seconds:02}"

def makeGraph(activity, fig, graph_data):
    start = datetime.fromtimestamp(activity.start_time)
    dt_str_1 = start.strftime("%A, %B %d, %Y at %I:%M %p")
    end = datetime.fromtimestamp(activity.end_time)
    dt_format = "%d-%b-%Y %H:%M:%S"
    total_seconds = int((end - start).total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    state = {'playing': False, 'current_time': 0}
    x_axis_unit = {'current': 'seconds'}
    speed_value = {'current': 1.0}
    updates_per_second = 10
    base_time_increment = 1.0 / updates_per_second    
    ui_elements = {}
    
    
    plot_container = ui.column().classes('w-full p-4 shadow-2 rounded-md border border-[#3545FF] bg-[#F5F5F5] dark:bg-[#0A0A0A] relative')

    sensor_types = [
        'Cushion',
        'FSR'
    ]

    dot_trace_indices = []

    def toggle_play():
        state['playing'] = not state['playing']
        if state['playing']:
            ui_elements['timer'].activate()
            ui_elements['play_pause_icon'].set_name('pause_circle')
        else:
            ui_elements['timer'].deactivate()
            ui_elements['play_pause_icon'].set_name('play_circle')

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

    def toggle_x_axis_unit(e):
        if x_axis_unit['current'] == 'seconds':
            x_axis_unit['current'] = 'minutes'
        else:
            x_axis_unit['current'] = 'seconds'
        update_x_axis()

    def update_x_axis():
        current_unit = x_axis_unit['current']

        for i, (index, sensor_data) in enumerate(graph_data[activity.activity_id].items()):
            line_idx = i * 2
            display_timestamps = get_display_values(sensor_data['timestamps'], current_unit)
            fig.data[line_idx].x = display_timestamps
        
        current_time = state["current_time"]
        display_current_time = current_time / 60 if current_unit == 'minutes' else current_time
        
        for i, (index, sensor_data) in enumerate(graph_data[activity.activity_id].items()):
            if i < len(dot_trace_indices):
                dot_idx = dot_trace_indices[i]
                fig.data[dot_idx].x = [display_current_time]
        
        fig.update_layout(xaxis_title=get_axis_label(current_unit))
        fig.update_xaxes(range=get_axis_range(current_unit))
        
        ui_elements['plot'].update()

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

        for i, (index, sensor_data) in enumerate(graph_data[activity.activity_id].items()):
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


    with plot_container:
        with ui.row().classes('w-full items-center justify-between'):
            with ui.grid(rows=2, columns=1).classes(replace=''):
                ui.label(f'{activity.activity_type} - {dt_str_1}').classes('text-lg font-semibold')      
                ui.label(activity.activity_id).classes('py-2 text-xs text-grey')

                                 
            with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                with ui.row().classes('items-center gap-2 w-4/6'):
                    ui.label('Speed:').classes('text-sm')
                    
                    def update_speed(e):
                        new = float(e.args)
                        speed_value["current"] = new
                        ui_elements['speed_label'].text = f"{new}x"
                    
                    ui.slider(min=0.1, max=100.0, step=0.1, value=1.0).props('label-always snap markers="[1, 5, 10, 25, 50, 100]"').classes('w-1/5').style('--q-primary: #FFB030').on('update:model-value', update_speed)
                    speed_label = ui.label("1.0x").classes('text-sm min-w-8')
                    ui_elements['speed_label'] = speed_label

                    with ui.row().classes('items-center gap-2'):
                        ui.label('Seconds').classes('text-sm')
                        ui.switch(value=False).on('update:model-value', toggle_x_axis_unit).style('--q-primary: #FFB030')
                        ui.label('Minutes').classes('text-sm')

                with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] p-2').on_click(toggle_play):
                    with ui.grid(columns=2).classes('w-full'):
                        with ui.column().classes('gap-0 items-start w-full'):
                            ui.label('Activity').classes('text-sm leading-tight m-0')
                            current_time_label = ui.label(format_current_time(state['current_time'])).classes('text-sm leading-tight m-0')
                            ui_elements['current_time_label'] = current_time_label
                        with ui.column().classes('items-end'):
                            play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;')
                            ui_elements['play_pause_icon'] = play_pause_icon
                


        current_unit = 'seconds'
        
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
            
            sensor_name = f"{sensor.location_name.capitalize() + " " + str(i + 1)} ({sensor_types[sensor.sensor_type]})"
            color = colors[i % len(colors)]
            timestamps = graph_data[activity.activity_id][activity_reading.reading_series_id]["timestamps"]
            display_timestamps = get_display_values(timestamps, current_unit)
            pressures = graph_data[activity.activity_id][activity_reading.reading_series_id]["signals"]
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

        setFigStyling(fig)
        fig.update_layout(xaxis_title=get_axis_label(current_unit))
        fig.update_xaxes(range=get_axis_range(current_unit))

        plot = ui.plotly(fig).classes('w-full h-[500px]')  
        ui_elements['plot'] = plot

    return plot_container, plot

def create() -> None:
    @ui.page("/activity")
    def activity():
        def handle_theme_change(e):
            print(e)

        ui.add_head_html('''
                <script>
                    window.matchMedia('(prefers-color-scheme: dark)').addListener(function (e) {
                    console.log(`changed to ${e.matches ? "dark" : "light"} mode`)
                    });
                </script>
            ''')

        app.storage.user['current_page'] = '/activity'
        ui.page_title("SocketFit Dashboard")
        ui.on('theme-change', lambda e: handle_theme_change(e))
        utilities.header()
        utilities.sidebar() 

        ee = utilities.ee
        @ee.on('dark-mode')
        def handle_dark(data):
            for id, fig in figs.items():
                setFigStyling(fig)
                plots[id].update()
                      
        # {activity_id: {activity_reading_id: {timestamps, signals, name}}}
        graph_data = {}
        # {activity_id: {pressure_min, pressure_max, duration}}
        activity_data = {}
        # checkboxes, for binding visibility of the graphs to
        activity_checkboxes = {}
        # plot cotnainer dictionary
        plot_containers = {}

        # Figure dictionary
        figs = {}
        plots = {}

        def toggle_graph_visibility(e):
            plot = plot_containers[activity_checkboxes[e.sender]]
            if e.value:
                plot.move(graphsContainer)
            else:
                plot.move(invisibleContainer)

        # Title bar
        with ui.row().classes('w-full'):
            patient = api.get_patient(
                patient_id=app.storage.user.get("selected_patient"), 
                token=app.storage.user.get('token')
            )

            with ui.row().classes('items-center gap-2 w-full'):
                ui.label(f"{patient.first_name} {patient.last_name}'s Activities").classes('text-xl font-semibold') 

            
        
        # Get graph data
        activities = api.get_activities(
            patient_id=app.storage.user.get("selected_patient"), 
            token=app.storage.user.get("token")
        )

        for activity in activities:
            start = datetime.fromtimestamp(activity.start_time)
            end = datetime.fromtimestamp(activity.end_time)

            total = (end - start).total_seconds()
            graph_data[activity.activity_id] = {}

            hours = int(total // 3600)
            minutes = int((total % 3600) // 60)
            seconds = int(total % 60)

            pressure_min, pressure_max = None, None

            activity_readings = api.get_activity_readings(
                app.storage.user.get("selected_patient"), 
                activity.activity_id, 
                app.storage.user.get("token")
            )

            for activity_reading in activity_readings:
                sensor = api.get_sensor(
                    app.storage.user.get("selected_patient"), 
                    activity_reading.sensor_id, 
                    app.storage.user.get("token")
                )
                
                sensor_name = f"{sensor.location_name.capitalize()} ({sensor.sensor_type})"

                pressure_readings = api.get_pressure_readings(
                    app.storage.user.get("selected_patient"), 
                    activity.activity_id, 
                    activity_reading.reading_series_id, 
                    app.storage.user.get("token")
                )

                timestamps = []
                pressures = []

                for pressure_reading in pressure_readings:
                    value = pressure_reading.pressure_value
                    if pressure_min is None or value < pressure_min:
                        pressure_min = round(value, 1)
                    if pressure_max is None or value > pressure_max:
                        pressure_max = round(value, 1)

                    time = datetime.fromtimestamp(pressure_reading.time)
                    time_from_start_seconds = (time - start).total_seconds()
                    time_from_start_seconds = max(0, min(time_from_start_seconds, total))

                    timestamps.append(time_from_start_seconds)
                    pressures.append(float(value))
                    
                combined = list(zip(timestamps, pressures))
                combined.sort(key=lambda x: x[0])
                timestamps, pressures = zip(*combined) if combined else ([], [])
                
                timestamps = list(timestamps)
                pressures = list(pressures)

                graph_data[activity.activity_id][activity_reading.reading_series_id] = {
                    "timestamps": timestamps,
                    'signals': pressures,
                    'name': sensor_name
                }

            activity_data[activity.activity_id] = {
                "pressure_min": pressure_min,
                "pressure_max": pressure_max,
                "duration": f'{hours}h{minutes}m{seconds}s',
            }

        # Activity container
        with ui.column().classes('w-full'):
            with ui.row().classes('w-full'):
                with ui.card().classes('w-full border rounded-md bg-[#F5F5F5] dark:bg-[#0A0A0A] border-[#3545FF]'):
                    with ui.card().classes('w-full shadow-0 p-0 items-start bg-[#F5F5F5] dark:bg-[#0A0A0A]'):        

                        with ui.grid(columns=14).classes('w-full rounded items-center'):
                            ui.label('Date').classes('col-span-4 font-bold')
                            ui.label('Activity').classes('col-span-2 font-bold')
                            ui.label('Duration').classes('col-span-2 font-bold')
                            ui.label('Pressure').classes('col-span-3 font-bold')
                            ui.label('Display').classes('col-span-3 font-bold')
                    
                    for activity in activities:
                        data = activity_data[activity.activity_id]
                       
                        with ui.grid(columns=14).classes('border-[1.5px] w-full border-[#2C25B2] rounded items-center'):
                            ui.label(datetime.fromtimestamp(activity.start_time).strftime("%A, %B %d, %Y at %I:%M %p")).classes('col-span-4')
                            ui.label(activity.activity_type).classes('col-span-2')
                            ui.label(data["duration"]).classes('col-span-2')
                            ui.label(f"{data["pressure_min"]} - {data["pressure_max"]}").classes('col-span-3')
                            checkbox = ui.checkbox('Display Activity', value=False, on_change=toggle_graph_visibility).style('--q-primary: #FFB030').classes('col-span-3')
                            activity_checkboxes[checkbox] = activity.activity_id
                    ui.space()
            
                # make graphs
                graphsContainer = ui.column().classes('w-full flex flex-row mt-4')
                invisibleContainer = ui.column().classes('w-full flex flex-row mt-4')
                invisibleContainer.set_visibility(False)
                with invisibleContainer:
                    for activity in activities: 
                            fig = go.Figure()
                            figs[activity.activity_id] = fig
                            plot_container, plot = makeGraph(activity, fig, graph_data)
                            plots[activity.activity_id] = plot
                            plot_containers[activity.activity_id] = plot_container
