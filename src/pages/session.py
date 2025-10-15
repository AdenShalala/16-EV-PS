from nicegui import ui, app
from datetime import datetime
from functools import partial
from collections import OrderedDict
import pages.utilities as utilities
import api

# getting activity and navigating
def activitypass(activity):
    app.storage.user['selected_activity'] = activity.activity_id
    ui.navigate.to("/activity")

def create() -> None:
    @ui.page('/patient/session')
    def session():
        app.storage.user['current_page'] = '/patient/session'
        ui.page_title("SocketFit Dashboard")
        utilities.header()

        actTypeList = ['All']

        activities = api.get_activities(patient_id=app.storage.user.get("selected_patient"), token=app.storage.user.get("token"))

        for activity in activities:
            print(activity)
            if activity.activity_type not in actTypeList:
                actTypeList.append(activity.activity_type)

        with ui.row().classes('w-full'):
            ui.label("Patient History").classes('text-xl font-semibold')
        with ui.row().classes('w-full h-full'):
            # left section with tree
            
            # with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
            #     utilities.session_tree()
            
            # main section
            with ui.card().classes('w-full h-full border border-[#2C25B2]') as main:
                # filter titles
                ui.label("Filters:")
                with ui.grid(columns=11).classes('w-full'):
                    ui.label("Activity").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                    ui.label("Duration (seconds)").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                    ui.label("Pressure Range").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                
                with ui.grid(columns=11).classes('w-full'):
                    activity_filter = ui.select(options=actTypeList, value=actTypeList[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                    duration_min = ui.number(label="Min", placeholder="Min", value=None).classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    duration_max = ui.number(label="Max", placeholder="Max", value=None).classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                    pressure_min = ui.number(label="Min", placeholder="Min", value=None).classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    pressure_max = ui.number(label="Max", placeholder="Max", value=None).classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                
                ui.label("Session List").classes('text-2xl')
                
                activity_container = ui.column().classes('w-full')
                
                def filter_activities():
                    """Filter and display activities based on current filter values"""
                    activity_container.clear()
                    
                    with activity_container:
                        with ui.row().classes('w-full'):
                            with ui.card().classes('w-9/10 border rounded-md border-[#3545FF]'):
                                with ui.grid(columns=24):
                                    ui.label('').classes('col-span-1')
                                    ui.label('Date').classes('col-span-3')
                                    ui.label('').classes('col-span-3')
                                    ui.label('Activity').classes('col-span-2')
                                    ui.label('').classes('col-span-3')
                                    ui.label('Duration').classes('col-span-2')
                                    ui.label('').classes('col-span-3')
                                    ui.label('Pressure').classes('col-span-2')
                                    ui.label('').classes('col-span-2')
                                    ui.label('').classes('col-span-3')
                                
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
                                    
                                    # Get pressure readings
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
                                    
                                    if activity_filter.value != 'All' and activity.activity_type != activity_filter.value:
                                        continue
                                    
                                    if duration_min.value is not None and total_seconds < duration_min.value:
                                        continue
                                    if duration_max.value is not None and total_seconds > duration_max.value:
                                        continue
                                    
                                    if pressure_min.value is not None and (maxSensor is None or maxSensor < pressure_min.value):
                                        continue
                                    if pressure_max.value is not None and (minSensor is None or minSensor > pressure_max.value):
                                        continue
                                    
                                    with ui.grid(columns=24).classes('border-[2px] border-[#2C25B2] h-16 rounded items-center'):
                                        ui.label('').classes('col-span-1')
                                        ui.label(utilities.normalize_to_str(activity.start_time)).classes('col-span-3')
                                        ui.label('').classes('col-span-3')
                                        ui.label(activity.activity_type).classes('col-span-2')
                                        ui.label('').classes('col-span-3')
                                        ui.label(f'{hours}h{minutes}m{seconds}s').classes('col-span-2')
                                        ui.label('').classes('col-span-3')
                                        ui.label(f"{minSensor} - {maxSensor}").classes('col-span-2')
                                        ui.button('View Activity').props('flat').classes(
                                            'col-span-5 text-white text-sm px-3 py-1 rounded-3xl bg-[#FFB030] h-1/2'
                                        ).on_click(partial(activitypass, activity))
                            ui.space()
                
                activity_filter.on_value_change(lambda: filter_activities())
                duration_min.on_value_change(lambda: filter_activities())
                duration_max.on_value_change(lambda: filter_activities())
                pressure_min.on_value_change(lambda: filter_activities())
                pressure_max.on_value_change(lambda: filter_activities())
                
                filter_activities()