from nicegui import ui, app
import pages.utilities as utilities
import plotly.graph_objects as go
from datetime import datetime
import plotly.colors as pc
import api
colors = pc.qualitative.Plotly

import database

def format_current_time(current_time):
    current_hours = int(current_time // 3600)
    current_minutes = int((current_time % 3600) // 60)
    current_seconds = int(current_time % 60)
    return f"{current_hours:02}:{current_minutes:02}:{current_seconds:02}"

def setFigStyling(fig):
    fig.update_layout(
        hovermode='x unified',
        autosize=True,
        showlegend=True,
    )

    if app.storage.user.get("dark_mode", False) == True:
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

sensor_types = ['Cushion','FSR']
def makeGraph(activity, figure, data):
    plot_data = {
        'playing': False,
        'current_time': 0,
        'speed': 1.0,
    }

    updates_per_second = 10
    base_time_increment = 1.0 / updates_per_second    
    ui_elements = {}

    total_seconds = (activity.end_time - activity.start_time)

    # toggle play/pause of graph
    def toggle_play():
        plot_data['playing'] = not plot_data['playing']
        if plot_data['playing']:
            ui_elements['timer'].activate()
            ui_elements['play_pause_icon'].set_name('pause_circle')
        else:
            ui_elements['timer'].deactivate()
            ui_elements['play_pause_icon'].set_name('play_circle')


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
        current_speed = plot_data["speed"]
        time_increment = base_time_increment * current_speed

        current_time = plot_data['current_time']
        current_time += time_increment
        
        if current_time >= total_seconds:
            current_time = 0
        
        plot_data['current_time'] = current_time

        ui_elements['current_time_label'].text = format_current_time(current_time)

        for i, (_, sensor_data) in enumerate(info["sensors"].items()):
            if i < len(dot_trace_indices):
                dot_idx = dot_trace_indices[i]
                
                signal_value = interpolate_signal(
                    sensor_data["timestamps"],
                    sensor_data["signals"], 
                    current_time
                )
                
                figure.data[dot_idx].x = [current_time]
                figure.data[dot_idx].y = [signal_value]

        ui_elements['playback_slider'].value = current_time
        ui_elements['plot'].update()
        ui_elements['plot']._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}


    def update_playback_slider(e):
        plot_data['current_time'] = e.args
        update_dots()

    info = data[activity.activity_id]
    dot_trace_indices = []

    plot_container = ui.column().classes('w-full p-4 rounded-md border border-[#3545FF] bg-[#F5F5F5] dark:bg-[#1d1d1d] relative')

    setFigStyling(figure)
    figure.update_layout(xaxis_title=f"Time (seconds)")
    figure.update_xaxes(range=[0, total_seconds])
    figure.update_yaxes(title_text='Pressure (kPa)')                        

    timer = ui.timer(interval=0.1, callback=update_dots, active=False)
    ui_elements['timer'] = timer

    # building plot container
    with plot_container:
        with ui.row().classes('w-full flex items-center justify-between'):
            with ui.grid(rows=2, columns=1).classes(replace=''):
                ui.label(f'{activity.activity_type} - {datetime.fromtimestamp(activity.start_time).strftime("%A, %B %d, %Y at %I:%M %p")}').classes('text-lg font-semibold')      
                ui.label(activity.activity_id).classes('py-2 text-xs text-grey')
                                
            with ui.grid(rows=1, columns=2).classes(replace='w-full flex justify-between'):
                with ui.row().classes('items-center gap-2 w-4/6'):
                    ui.label('Speed:').classes('text-sm')
                    
                    def update_speed(e):
                        if e.args:
                            new = float(e.args)
                        else:
                            new = 0.0
                        plot_data["speed"] = new
                        ui_elements['speed_label'].text = f"{new}x"
                    speed_slider = ui.slider(min=0.1, max=100.0, step=0.1, value=1.0).props('label-always snap markers="[1, 5, 10, 25, 50, 100]"').classes('w-1/5').style('--q-primary: #FFB030').on('update:model-value', update_speed)
                    speed_label = ui.number(value=1.0, precision=1, min=0.1, max=100).classes('text-sm min-w-12 w-12').bind_value(speed_slider).on('update:model-value', update_speed)
                    ui_elements['speed_label'] = speed_label

                with ui.button(color='#FFB030').classes('rounded-md text-white flex justify-between w-[230px] p-2').on_click(toggle_play):
                    with ui.grid(columns=2).classes('w-full'):
                        with ui.column().classes('gap-0 items-start w-full'):
                            ui.label('Activity').classes('text-sm leading-tight m-0')
                            current_time_label = ui.label(format_current_time(plot_data['current_time'])).classes('text-sm leading-tight m-0')
                            ui_elements['current_time_label'] = current_time_label
                        with ui.column().classes('items-end'):
                            play_pause_icon = ui.icon('play_circle').classes('text-4xl text-right').style('font-size: 40px;')
                            ui_elements['play_pause_icon'] = play_pause_icon
                

        for i, (_, sensor_data) in enumerate(info["sensors"].items()):     
            color = colors[i % len(colors)]
            sensor_name = f"{sensor_data["location_name"].capitalize() + " " + str(i + 1)} ({sensor_types[sensor_data["sensor_type"]]})"

            figure.add_trace(go.Scatter(
                x=sensor_data["timestamps"],
                y=sensor_data["signals"],
                name=sensor_name,
                line=dict(color=color)
            ))       

            figure.add_trace(go.Scatter(
                x=[sensor_data["timestamps"][0]],
                y=[sensor_data["signals"][0]],
                mode='markers',
                hoverinfo='skip',
                marker=dict(size=10, color=color),
                name=sensor_name,
                showlegend=False
            ))                                            

            dot_trace_indices.append(len(figure.data) - 1)             
            

        plot = ui.plotly(figure)
        plot.classes('w-full h-[500px]')  
        plot._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}
        ui_elements['plot'] = plot
        playback_slider = ui.slider(min=0, max=total_seconds).classes('w-full').style('--q-primary: #FFB030')
        playback_slider.on('update:model-value', lambda e: update_playback_slider(e), trailing_events=False)
        ui_elements['playback_slider'] = playback_slider
        return plot_container, plot

def create() -> None:
    # dashboard page
    @ui.page("/dashboard")
    def dashboard():
        app.storage.user['current_page'] = '/dashboard'
        ui.page_title("SocketFit Dashboard")

        token = app.storage.user.get("token")
        selected_patient = app.storage.user.get("selected_patient")
        patient = api.get_patient(selected_patient, token)

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
                
            for id, container in plot_containers.items():
                if container.visible:
                    setFigStyling(figs[id])
                    plots[id].update()
                    plots[id]._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}

    
        # setting up header 
        def header():
            me = api.get_me(token=app.storage.user.get("token"))
            dark = ui.dark_mode(app.storage.user.get("dark_mode", False))

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
        left_drawer = utilities.sidebar() 
        arrow = utilities.arrow(left_drawer)

        # updating plots on sidebar toggle
        def update_plots():
            def update():
                for id, container in plot_containers.items():
                    if container.visible:
                        for i in range(100):
                            plots[id].update()
                            plots[id]._props['options']['config'] = {'modeBarButtonsToRemove': ['select2d', 'lasso2d'], 'displaylogo': False}
                
                timer.cancel()

            timer = ui.timer(interval=0.01, callback=update, immediate=True)


        arrow.on_click(lambda: update_plots())

        activity_checkboxes = {}

        figs = {}
        plots = {}
        plot_containers = {}

        filter_icons = {}
        filter_data = {'current': "", 'descending': True}

        data = {}

        # title bar
        with ui.row().classes('w-full'):
            with ui.row().classes('items-center gap-2 w-full'):
                ui.label(f"{patient.first_name} {patient.last_name}'s Activities").classes('text-xl font-semibold')  
        
        # get graph data
        activities = api.get_activities(selected_patient, token)

        for activity in activities:
            id = activity.activity_id
            
            # really unfortunate to not use api call here
            # Super bad but  its like 4x slower with the api request
            result = database.get_pressure_readings_for_activities(activity.activity_id, selected_patient)

            start_time = activity.start_time

            total = (activity.end_time - start_time)

            hours = int(total // 3600)
            minutes = int((total % 3600) // 60)
            seconds = int(total % 60)

            data[id] = {"sensors": {}, "min": None, "max": None, "duration": f'{hours}h{minutes}m{seconds}s'}

            for i in result:
                reading_series_id, sensor_id, location_name, sensor_type, time, pressure_value = i

                if not reading_series_id in data[id]["sensors"]:
                    data[id]["sensors"][reading_series_id] = {"timestamps": [], "signals": [], "sensor_id": sensor_id, "location_name": location_name, "sensor_type": sensor_type}

                if data[id]["min"] is None or pressure_value < data[id]["min"]:
                    data[id]["min"] = int(round(pressure_value, 1))
                if data[id]["max"] is None or pressure_value > data[id]["max"]:
                    data[id]["max"] = int(round(pressure_value, 1))

                data[id]["sensors"][reading_series_id]["timestamps"].append(time - start_time)
                data[id]["sensors"][reading_series_id]["signals"].append(float(pressure_value))           
        
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
            elif filter_type == "Pressure (Min - Max)":
                filtered_activities.sort(
                    key=lambda a: data[a.activity_id]['max'] if data[a.activity_id]['max'] is not None else 0,
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
                    info = data[activity.activity_id]
                    visible = visibility_state.get(activity.activity_id, False)
            
                    with ui.grid(columns=14).classes('px-2 border-[1.5px] w-full border-[#3545FF] rounded items-center'):
                        ui.label(datetime.fromtimestamp(activity.start_time).strftime("%A, %B %d, %Y at %I:%M %p")).classes('col-span-4')
                        ui.label(activity.activity_type).classes('col-span-2')
                        ui.label(info["duration"]).classes('col-span-2')
                        ui.label(f"{info["min"]} - {info["max"]}").classes('col-span-3')
                        
                        # create a closure to capture the correct activity_id
                        def make_toggle_handler(activity_id):
                            def handler(e):
                                plot = plot_containers[activity_id]
                                if e.value:
                                    plot.set_visibility(True)
                                    plot.move(graphsContainer)
                                    plot.update()
                                else:
                                    plot.set_visibility(False)
                                    plot.move(invisibleContainer)
                                    plot.update()
                            return handler
                        
                        checkbox = ui.checkbox(
                            'Display Activity', 
                            value=visible, 
                            on_change=make_toggle_handler(activity.activity_id)
                        ).style('--q-primary: #FFB030').classes('col-span-3')
                        
                        activity_checkboxes[checkbox] = activity.activity_id

        # activity container
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
                                ui.label("Pressure (Min - Max)").classes('font-bold dark:text-white')
                                filter_icons["Pressure"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Pressure"].set_visibility(False)
                            with ui.button(on_click=lambda: filter_activities("Display")).classes('px-0 col-span-3').props('flat no-caps color=black align="left"'):
                                ui.label("Display").classes('font-bold dark:text-white')
                                filter_icons["Display"] = ui.icon('arrow_drop_down').classes('dark:!text-white')
                                filter_icons["Display"].set_visibility(False)
                    
                    activity_container = ui.row().classes('w-full')
                    filter_activities("Date")

                    ui.space()        

                graphsContainer = ui.column().classes('w-full flex flex-row mt-4')
                invisibleContainer = ui.column().classes('w-full flex flex-row mt-4')
                invisibleContainer.set_visibility(False)
                with invisibleContainer:
                    for activity in activities:
                            fig = go.Figure()
                            figs[activity.activity_id] = fig
                            plot_container, plot = makeGraph(activity, fig, data)
                            plots[activity.activity_id] = plot
                            plot_containers[activity.activity_id] = plot_container
                            plot_container.set_visibility(False)