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

        #app.storage.user['actTypeList'] = ['All']
        #app.storage.user['activityList'] = []

        activities = api.get_activities(patient_id=app.storage.user.get("selected_patient"), token=app.storage.user.get("token"))

        # for activity in activities:
        #     #app.storage.user['activityList'].append(app.storage.user['activity'])
        #     # adding unique activity types to list
        #     if app.storage.user.get('activity').type not in app.storage.user.get('actTypeList'):
        #         app.storage.user['actTypeList'].append(app.storage.user['activity'].type)

        with ui.row().classes('w-full'):
            ui.label("User History").classes('text-xl font-semibold ml-[21%]')
        with ui.row().classes('w-full h-full'):
            # left section with tree
            with ui.card().classes('w-1/5 h-full border border-[#2C25B2]') as patients:
                utilities.session_tree()
            # main section
            with ui.card().classes('w-3/4 h-full border border-[#2C25B2]') as main:
                # filter titles
                ui.label("Filters:")
                with ui.grid(columns=11).classes('w-full'):
                    ui.label("Activity").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                    ui.label("Duration").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                    ui.label("Pressure Range").classes('col-span-2')
                    ui.label('').classes('col-span-1')
                    ui.label('Pressure Tolerance').classes('col-span-2')
                # filter boxes
                with ui.grid(columns=11).classes('w-full'):
                    #ui.select(options=app.storage.user.get('actTypeList'), value=app.storage.user.get('actTypeList', [])[0]).classes('col-span-2 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                    ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                    ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.label('').classes('col-span-1')
                    ui.number(label="Min", placeholder="Min").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                    ui.number(label="Max", placeholder="Max").classes('col-span-1 w-full border rounded-md border-[#3545FF]')
                ui.label("Session List").classes('text-2xl')
                with ui.row().classes('w-full'):
                    # titles for session activities
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
                            hours, minutes, seconds = 0, 0, 0
                            minSensor, maxSensor = None, None
                            dt_str1 = utilities.normalize_to_str(activity.start_time)
                            dt_str2 = utilities.normalize_to_str(activity.end_time)

                            dt_format = "%d-%b-%Y %H:%M:%S"

                            dt1 = datetime.strptime(dt_str1, dt_format)
                            dt2 = datetime.strptime(dt_str2, dt_format)

                            total_seconds = int((dt2 - dt1).total_seconds())
                            #app.storage.user['total_seconds'] = total_seconds

                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            seconds = total_seconds % 60
                            
                            # finding min and max sensor signal values
                            # current_activity = app.storage.user['current_activity']  # Store reference for cleaner access

                            readings = api.get_activity_readings(app.storage.user.get("selected_patient"), activity.activity_id, app.storage.user.get("token"))
                            
                            for reading in readings:
                                pressure = api.get_pressure_readings(app.storage.user.get("selected_patient"), activity.activity_id, reading.reading_series_id, app.storage.user.get("token"))

                                for x in pressure:
                                    value = float(x.pressure_value)

                                    if minSensor is None or value < minSensor:
                                        minSensor = round(value, 1)

                                    if maxSensor is None or value > maxSensor:
                                        maxSensor = round(value, 1)


                            # creating row for each activity
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
