from nicegui import ui, app
import pages.utilities as utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc
import api
colors = pc.qualitative.Plotly

# get display values based on selected unit
def get_display_values(timestamps_in_seconds, unit):
    if unit == 'minutes':
        return [t / 60 for t in timestamps_in_seconds]
    return timestamps_in_seconds

# set figure styling based on dark mode
def setFigStyling(fig):
    fig.update_layout(
        hovermode='x unified',
        autosize=True,
        showlegend=True,
    )

    if app.storage.user.get('dark_mode') == True:
        fig.update_layout(
            plot_bgcolor='#1d1d1d',
            paper_bgcolor='#1d1d1d',
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

# format current time for display
def format_current_time(current_time):
    current_hours = int(current_time // 3600)
    current_minutes = int((current_time % 3600) // 60)
    current_seconds = int(current_time % 60)
    return f"{current_hours:02}:{current_minutes:02}:{current_seconds:02}"

# make graph for activity
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
    
    
    plot_container = ui.column().classes('w-full p-4 rounded-md border border-[#3545FF] bg-[#F5F5F5] dark:bg-[#1d1d1d] relative')

    sensor_types = [
        'Cushion',
        'FSR'
    ]

    dot_trace_indices = []

    # toggle play/pause of graph
    def toggle_play():
        state['playing'] = not state['playing']
        if state['playing']:
            ui_elements['timer'].activate()
            ui_elements['play_pause_icon'].set_name('pause_circle')
        else:
            ui_elements['timer'].deactivate()
            ui_elements['play_pause_icon'].set_name('play_circle')

    # get display values based on selected unit
    def get_display_values(timestamps_in_seconds, unit):
        if unit == 'minutes':
            return [t / 60 for t in timestamps_in_seconds]
        return timestamps_in_seconds

    # get axis label based on unit
    def get_axis_label(unit):
        return f"Time ({unit})"

    # get axis range based on unit
    def get_axis_range(unit):
        if unit == 'minutes':
            return [0, total_seconds / 60]
        return [0, total_seconds]

    # toggle x-axis unit between seconds and minutes
    def toggle_x_axis_unit(e):
        if x_axis_unit['current'] == 'seconds':
            x_axis_unit['current'] = 'minutes'
        else:
            x_axis_unit['current'] = 'seconds'
        update_x_axis()

    # update x-axis based on selected unit
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

        # removing unwanted plotly buttons
        ui_elements['plot']._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoscale'], 'displaylogo': False}

    # interpolate signal value at target time
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

    # update dot positions based on current time
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
        ui_elements['plot']._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoscale'], 'displaylogo': False}

    timer = ui.timer(interval=0.1, callback=update_dots, active=False)
    ui_elements['timer'] = timer

    # building plot container
    with plot_container:
        with ui.row().classes('w-full flex items-center justify-between'):
            with ui.grid(rows=2, columns=1).classes(replace=''):
                ui.label(f'{activity.activity_type} - {dt_str_1}').classes('text-lg font-semibold')      
                ui.label(activity.activity_id).classes('py-2 text-xs text-grey')

                                 
            with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                with ui.row().classes('items-center gap-2 w-4/6'):
                    ui.label('Speed:').classes('text-sm')
                    
                    # updating playing speed
                    def update_speed(e):
                        if e.args:
                            new = float(e.args)
                        else:
                            new = 0.0
                        speed_value["current"] = new
                        ui_elements['speed_label'].text = f"{new}x"
                    speed_slider = ui.slider(min=0.1, max=100.0, step=0.1, value=1.0).props('label-always snap markers="[1, 5, 10, 25, 50, 100]"').classes('w-1/5').style('--q-primary: #FFB030').on('update:model-value', update_speed)
                    speed_label = ui.number(value=1.0, precision=1, min=0.1, max=100).classes('text-sm min-w-12 w-12').bind_value(speed_slider).on('update:model-value', update_speed)
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
        
        # getting readings for activity
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

        # setting figure styling 
        setFigStyling(fig)
        fig.update_layout(xaxis_title=get_axis_label(current_unit))
        fig.update_xaxes(range=get_axis_range(current_unit))
        fig.update_yaxes(title_text='Pressure (kPa)')

        plot = ui.plotly(fig).classes('w-full h-[500px]')  
        plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoscale'], 'displaylogo': False}
        ui_elements['plot'] = plot

    return plot_container, plot

def create() -> None:
    # dashboard page
    @ui.page("/dashboard")
    def dashboard():
        # setting current page in storage
        app.storage.user['current_page'] = '/dashboard'
        # adding in page title
        ui.page_title("SocketFit Dashboard")

        figs = {}
        plots = {}

        def handle_dark(data):
            for id, fig in figs.items():
                setFigStyling(fig)
                plots[id].update()
                plots[id]._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoscale'], 'displaylogo': False}

        # GOD THIS IS ANNOYING
        # We have to replace the header in THIS SPECIFIC PAGE BECAUSE OF PLOTLY :)
        def toggle_dark_mode(value, button, dark):
            if value == True:
                app.storage.user['dark_mode'] = False
                dark.disable()
                button.name='dark_mode'
            else:
                app.storage.user['dark_mode'] = True
                dark.enable()
                button.name='light_mode'
                
            handle_dark(value)

        # setting up header
        def header():
            dark = ui.dark_mode(app.storage.user.get("dark_mode", False))            
            me = api.get_me(token=app.storage.user.get("token"))

            with ui.header(elevated=False).classes('bg-[#ffffff] dark:bg-[#1d1d1d] shadow-xl'):
                with ui.row().classes('w-full justify-between items-center px-2'):
                    with ui.row().classes('items-center gap-4'):
                        with ui.link(target='/'):
                            ui.image('/assets/dashboard.png').classes('h-[40px] w-[150px]')


                    with ui.row().classes('items-center gap-4'):
                        with ui.button().classes('px-0').props('flat no-caps color=black align="left"').on_click(lambda: ui.navigate.to('/account')):
                            ui.label(f'{me.first_name} {me.last_name} [{type(me).__name__}]').classes(' font-bold !text-gray-600 dark:!text-gray-400')
                        dark_button = ui.icon('dark_mode').on('click', lambda: toggle_dark_mode(app.storage.user.get("dark_mode", False), dark_button, dark)).classes('!text-gray-600 dark:!text-gray-400 cursor-pointer text-3xl')
                        if app.storage.user.get('dark_mode') == True:
                            dark_button.name='light_mode'
                        elif app.storage.user.get('dark_mode') == False:
                            dark_button.name='dark_mode'

        header()

        # setting up sidebar and arrow
        left_drawer = utilities.sidebar() 
        arrow = utilities.arrow(left_drawer)

        # updating plots on sidebar toggle
        def update_plots():
            def test():
                for i in range(100):
                    for id, plot in plots.items():
                        plot.update()
                        plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d', 'autoscale'], 'displaylogo': False}
                
                timer.cancel()

            timer = ui.timer(interval=0.01, callback=test, immediate=True)


        arrow.on_click(lambda: update_plots())
                      
        # {activity_id: {activity_reading_id: {timestamps, signals, name}}}
        graph_data = {}
        # {activity_id: {pressure_min, pressure_max, duration}}
        activity_data = {}
        # checkboxes, for binding visibility of the graphs to
        activity_checkboxes = {}
        # plot cotnainer dictionary
        plot_containers = {}

        filter_icons = {}

        filter_data = {'current': "", 'descending': True}

        # toggle graph visibility
        def toggle_graph_visibility(e):
            plot = plot_containers[activity_checkboxes[e.sender]]
            if e.value:
                plot.move(graphsContainer)
            else:
                plot.move(invisibleContainer)

        # title bar
        with ui.row().classes('w-full'):
            patient = api.get_patient(
                patient_id=app.storage.user.get("selected_patient"), 
                token=app.storage.user.get('token')
            )

            with ui.row().classes('items-center gap-2 w-full'):
                ui.label(f"{patient.first_name} {patient.last_name}'s Activities").classes('text-xl font-semibold')  
        
        # get graph data
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

        # filtering activities
        def filter_activities(filter_type: str):
            if filter_data['current'] == filter_type:
                filter_data['descending'] = not filter_data['descending']
            else:
                filter_data['current'] = filter_type
                filter_data['descending'] = True
            
            # update icon visibility and direction
            for key, icon in filter_icons.items():
                if key == filter_type:
                    icon.set_visibility(True)
                    if filter_data['descending']:
                        icon.name = 'arrow_drop_down'
                    else:
                        icon.name = 'arrow_drop_up'
                else:
                    icon.set_visibility(False)
            
            filtered_activities = activities.copy()
            
            visibility_state = {}
            for checkbox, act_id in activity_checkboxes.items():
                visibility_state[act_id] = checkbox.value

            # sort activities based on filter type
            if filter_type == "Date":
                filtered_activities.sort(key=lambda a: a.start_time, reverse=filter_data['descending'])
            elif filter_type == "Activity":
                filtered_activities.sort(key=lambda a: a.activity_type, reverse=filter_data['descending'])
            elif filter_type == "Duration":
                filtered_activities.sort(
                    key=lambda a: (datetime.fromtimestamp(a.end_time) - datetime.fromtimestamp(a.start_time)).total_seconds(),
                    reverse=filter_data['descending']
                )
            elif filter_type == "Pressure":
                filtered_activities.sort(
                    key=lambda a: activity_data[a.activity_id]['pressure_max'] if activity_data[a.activity_id]['pressure_max'] is not None else 0,
                    reverse=filter_data['descending']
                )
            elif filter_type == "Display":
                # sort by checkbox state
                filtered_activities.sort(
                    key=lambda a: visibility_state.get(a.activity_id, False),
                    reverse=filter_data['descending']
                )        
            
            # clear and repopulate activity container
            activity_container.clear()
            activity_checkboxes.clear()

            with activity_container:
                for activity in filtered_activities:
                    data = activity_data[activity.activity_id]
                    visible = visibility_state.get(activity.activity_id, False)
            
                    with ui.grid(columns=14).classes('px-2 border-[1.5px] w-full border-[#3545FF] rounded items-center'):
                        ui.label(datetime.fromtimestamp(activity.start_time).strftime("%A, %B %d, %Y at %I:%M %p")).classes('col-span-4')
                        ui.label(activity.activity_type).classes('col-span-2')
                        ui.label(data["duration"]).classes('col-span-2')
                        ui.label(f"{data["pressure_min"]} - {data["pressure_max"]}").classes('col-span-3')
                        
                        # create a closure to capture the correct activity_id
                        def make_toggle_handler(activity_id):
                            def handler(e):
                                plot = plot_containers[activity_id]
                                if e.value:
                                    plot.move(graphsContainer)
                                else:
                                    plot.move(invisibleContainer)
                            return handler
                        
                        checkbox = ui.checkbox(
                            'Display Activity', 
                            value=visible, 
                            on_change=make_toggle_handler(activity.activity_id)
                        ).style('--q-primary: #FFB030').classes('col-span-3')
                        
                        activity_checkboxes[checkbox] = activity.activity_id
            

        # qctivity container
        with ui.column().classes('w-full'):
            with ui.row().classes('w-full'):
                with ui.card().classes('w-full border rounded-md bg-[#F5F5F5] dark:bg-[#1d1d1d] border-[#2C25B2] no-shadow'):
                    with ui.card().classes('no-shadow w-full 0 p-0 items-start bg-[#F5F5F5] dark:bg-[#1d1d1d]'):        

                        with ui.grid(columns=14).classes('px-2 w-full rounded items-center'):
                            with ui.button(on_click=lambda: filter_activities("Date")).classes('px-0 col-span-4').props('flat no-caps color=black align="left"'):
                                ui.label("Date").classes('font-bold dark:text-white')
                                filter_icons["Date"] = ui.icon('arrow_drop_down').classes('dark:!text-white').props('flat')
                            with ui.button(on_click=lambda: filter_activities("Activity")).classes('px-0 col-span-2').props('flat no-caps color=black align="left"'):
                                ui.label("Activity").classes('font-bold dark:text-white')
                                filter_icons["Activity"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Activity"].set_visibility(False)
                            with ui.button(on_click=lambda: filter_activities("Duration")).classes('px-0 col-span-2').props('flat no-caps color=black align="left"'):
                                ui.label("Duration").classes('font-bold dark:text-white')
                                filter_icons["Duration"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Duration"].set_visibility(False)
                            with ui.button(on_click=lambda: filter_activities("Pressure")).classes('px-0 col-span-3').props('flat no-caps color=black align="left"'):
                                ui.label("Pressure").classes('font-bold dark:text-white')
                                filter_icons["Pressure"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Pressure"].set_visibility(False)
                            with ui.button(on_click=lambda: filter_activities("Display")).classes('px-0 col-span-3').props('flat no-caps color=black align="left"'):
                                ui.label("Display").classes('font-bold dark:text-white')
                                filter_icons["Display"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Display"].set_visibility(False)
                    
                    activity_container = ui.row().classes('w-full')
                    filter_activities("Date")

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
